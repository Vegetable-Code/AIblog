# -*- coding: utf-8 -*-
"""Storage abstraction layer - supports S3-compatible backends (R2 / AWS S3 / MinIO) and local filesystem fallback."""
import os
import logging
import tempfile

import boto3
from botocore.config import Config as BotoConfig

from .config import settings

logger = logging.getLogger(__name__)


def _get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION or "auto",
        config=BotoConfig(signature_version="s3v4", connect_timeout=10, read_timeout=30),
    )


def upload_fileobj(fileobj, key):
    if _s3_configured():
        client = _get_s3_client()
        client.upload_fileobj(fileobj, settings.S3_BUCKET_NAME, key)
        return _s3_url(key)
    return _local_save(fileobj, key)


def upload_local(path, key):
    if _s3_configured():
        client = _get_s3_client()
        client.upload_file(path, settings.S3_BUCKET_NAME, key)
        return _s3_url(key)
    return _local_copy(path, key)


def get_url(key):
    if _s3_configured():
        return _s3_url(key)
    return "/uploads/" + key


def delete(key):
    if _s3_configured():
        client = _get_s3_client()
        client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    else:
        _local_delete(key)


def _s3_configured():
    return bool(
        settings.S3_ENDPOINT
        and settings.S3_ACCESS_KEY_ID
        and settings.S3_SECRET_ACCESS_KEY
        and settings.S3_BUCKET_NAME
    )


def _s3_url(key):
    public = (settings.S3_PUBLIC_URL or "").rstrip("/")
    if public:
        return public + "/" + key
    return "/uploads/" + key


def _local_root():
    root = os.environ.get(
        "UPLOAD_ROOT",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "uploads"),
    )
    os.makedirs(root, exist_ok=True)
    return root


def _local_save(fileobj, key):
    dest = os.path.join(_local_root(), key)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(fileobj.read())
    return "/uploads/" + key


def _local_copy(path, key):
    import shutil
    dest = os.path.join(_local_root(), key)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(path, dest)
    return "/uploads/" + key


def _local_delete(key):
    path = os.path.join(_local_root(), key)
    if os.path.exists(path):
        os.remove(path)


def create_temp_dir():
    return tempfile.mkdtemp(prefix="blog_import_")
