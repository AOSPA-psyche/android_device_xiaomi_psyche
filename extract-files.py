#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .binary_regex_replace('gettid: ', 'gettid: 1'),
    'vendor/lib/hw/audio.primary.psyche.so': blob_fixup()
        .binary_regex_replace(
            b'/vendor/lib/liba2dpoffload.so',
            b'liba2dpoffload_psyche.so\x00\x00\x00\x00\x00',
        ),
    'vendor/lib64/camera/components/com.mi.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so')
    'vendor/lib64/mediadrm/libwvdrmengine.so': blob_fixup()
        .add_needed('libcrypto_shim.so')
}  # fmt: skip

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libgrallocutils',
    ): lib_fixup_remove,
}

namespace_imports = [
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
    'vendor/qcom/common',
]

module = ExtractUtilsModule(
    'psyche',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sm8250-common', module.vendor)
    utils.run()
