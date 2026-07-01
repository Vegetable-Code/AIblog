#!/usr/bin/env python3
import os
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core import storage


def get_upload_root():
    return os.environ.get(
        "UPLOAD_ROOT",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads"),
    )


def find_local_uids(upload_root):
    pdfs_dir = os.path.join(upload_root, "pdfs")
    if not os.path.isdir(pdfs_dir):
        return set()
    return {d for d in os.listdir(pdfs_dir) if os.path.isdir(os.path.join(pdfs_dir, d))}


def find_db_uids(engine):
    uid_map = {}
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, content_html, cover_image FROM posts WHERE content_html LIKE '%/uploads/pdfs/%'")
        ).fetchall()
    for row in rows:
        post_id, html, cover = row
        for m in re.finditer(r"/uploads/pdfs/([a-f0-9]+)/", html or ""):
            uid = m.group(1)
            uid_map.setdefault(uid, []).append(post_id)
        if cover and "/uploads/pdfs/" in cover:
            m = re.search(r"/uploads/pdfs/([a-f0-9]+)/", cover)
            if m:
                uid = m.group(1)
                uid_map.setdefault(uid, []).append(post_id)
    return uid_map


def migrate_uids(uid_map, local_uids, upload_root, engine, dry_run):
    any_fail = False
    for uid, post_ids in sorted(uid_map.items()):
        local_dir = os.path.join(upload_root, "pdfs", uid)
        files_exist = uid in local_uids

        if files_exist:
            logger.info("UID %s - local files FOUND (%d post(s))", uid, len(post_ids))
            if not dry_run:
                for fname in os.listdir(local_dir):
                    fpath = os.path.join(local_dir, fname)
                    if os.path.isfile(fpath):
                        key = "pdfs/" + uid + "/" + fname
                        try:
                            url = storage.upload_local(fpath, key)
                            logger.info("  Uploaded: %s -> %s", fname, url)
                        except Exception as e:
                            logger.error("  Failed to upload %s: %s", fname, e)
                            any_fail = True
        else:
            logger.warning("UID %s - local files MISSING (updating URLs only)", uid)

        prefix = "/uploads/pdfs/" + uid
        new_prefix = storage.get_url("pdfs/" + uid).rstrip("/")

        with engine.begin() as conn:
            posts = conn.execute(
                text("SELECT id, content_html, cover_image FROM posts WHERE id = ANY(:ids)"),
                {"ids": post_ids},
            ).fetchall()
            for row in posts:
                pid, html, cover = row
                updates = {}
                if html and prefix in html:
                    updates["content_html"] = html.replace(prefix, new_prefix)
                if cover and prefix in cover:
                    updates["cover_image"] = cover.replace(prefix, new_prefix)
                if updates:
                    if dry_run:
                        logger.info("  [DRY-RUN] Post %d would update: %s", pid, list(updates.keys()))
                    else:
                        updates["pid"] = pid
                        conn.execute(
                            text("UPDATE posts SET content_html = :content_html, cover_image = :cover_image WHERE id = :pid"),
                            updates,
                        )
                        logger.info("  Post %d updated: %s", pid, list(updates.keys()))
                else:
                    logger.info("  Post %d - no changes needed", pid)
    return any_fail


if __name__ == "__main__":
    dry_run = "--execute" not in sys.argv
    upload_root = get_upload_root()
    logger.info("Upload root: %s", upload_root)
    logger.info("S3 configured: %s", storage._s3_configured())

    engine = create_engine(settings.DATABASE_URL)
    local_uids = find_local_uids(upload_root)
    uid_map = find_db_uids(engine)

    if not uid_map:
        logger.info("No posts with /uploads/pdfs/ URLs found. Nothing to migrate.")
        sys.exit(0)

    logger.info("Found %d unique UIDs in DB, %d have local files", len(uid_map), len(local_uids & set(uid_map.keys())))

    if dry_run:
        logger.info("=== DRY RUN (pass --execute to apply) ===")

    fail = migrate_uids(uid_map, local_uids, upload_root, engine, dry_run)

    if dry_run:
        logger.info("Run with --execute to apply changes.")
    elif fail:
        logger.warning("Migration completed with some errors.")
    else:
        logger.info("Migration completed successfully.")
