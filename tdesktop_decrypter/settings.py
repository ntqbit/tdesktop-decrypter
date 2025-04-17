from typing import Any, Dict, Tuple
from io import BytesIO
from enum import Enum

from tdesktop_decrypter.qt import (
    read_qt_int32,
    read_qt_uint64,
    read_qt_byte_array,
    read_qt_utf8,
)


class SettingsReadException(Exception):
    pass


class SettingsBlock(Enum):
    dbiKey = 0x00
    dbiUser = 0x01

    dbiDcOptionOldOld = 0x02
    dbiChatSizeMaxOld = 0x03
    dbiMutePeerOld = 0x04
    dbiSendKeyOld = 0x05
    dbiAutoStart = 0x06
    dbiStartMinimized = 0x07
    dbiSoundFlashBounceNotifyOld = 0x08
    dbiWorkModeOld = 0x09
    dbiSeenTrayTooltip = 0x0A
    dbiDesktopNotifyOld = 0x0B
    dbiAutoUpdate = 0x0C
    dbiLastUpdateCheck = 0x0D
    dbiWindowPositionOld = 0x0E
    dbiConnectionTypeOldOld = 0x0F

    dbiDefaultAttach = 0x11
    dbiCatsAndDogsOld = 0x12
    dbiReplaceEmojiOld = 0x13
    dbiAskDownloadPathOld = 0x14
    dbiDownloadPathOldOld = 0x15
    dbiScaleOld = 0x16
    dbiEmojiTabOld = 0x17
    dbiRecentEmojiOldOldOld = 0x18
    dbiLoggedPhoneNumberOld = 0x19
    dbiMutedPeersOld = 0x1A

    dbiNotifyViewOld = 0x1C
    dbiSendToMenu = 0x1D
    dbiCompressPastedImageOld = 0x1E
    dbiLangOld = 0x1F
    dbiLangFileOld = 0x20
    dbiTileBackgroundOld = 0x21
    dbiAutoLockOld = 0x22
    dbiDialogLastPath = 0x23
    dbiRecentEmojiOldOld = 0x24
    dbiEmojiVariantsOldOld = 0x25
    dbiRecentStickers = 0x26
    dbiDcOptionOld = 0x27
    dbiTryIPv6Old = 0x28
    dbiSongVolumeOld = 0x29
    dbiWindowsNotificationsOld = 0x30
    dbiIncludeMutedOld = 0x31
    dbiMegagroupSizeMaxOld = 0x32
    dbiDownloadPathOld = 0x33
    dbiAutoDownloadOld = 0x34
    dbiSavedGifsLimitOld = 0x35
    dbiShowingSavedGifsOld = 0x36
    dbiAutoPlayOld = 0x37
    dbiAdaptiveForWideOld = 0x38
    dbiHiddenPinnedMessagesOld = 0x39
    dbiRecentEmojiOld = 0x3A
    dbiEmojiVariantsOld = 0x3B
    dbiDialogsModeOld = 0x40
    dbiModerateModeOld = 0x41
    dbiVideoVolumeOld = 0x42
    dbiStickersRecentLimitOld = 0x43
    dbiNativeNotificationsOld = 0x44
    dbiNotificationsCountOld = 0x45
    dbiNotificationsCornerOld = 0x46
    dbiThemeKeyOld = 0x47
    dbiDialogsWidthRatioOld = 0x48
    dbiUseExternalVideoPlayerOld = 0x49
    dbiDcOptionsOld = 0x4A
    dbiMtpAuthorization = 0x4B
    dbiLastSeenWarningSeenOld = 0x4C
    dbiSessionSettings = 0x4D
    dbiLangPackKey = 0x4E
    dbiConnectionTypeOld = 0x4F
    dbiStickersFavedLimitOld = 0x50
    dbiSuggestStickersByEmojiOld = 0x51
    dbiSuggestEmojiOld = 0x52
    dbiTxtDomainStringOldOld = 0x53
    dbiThemeKey = 0x54
    dbiTileBackground = 0x55
    dbiCacheSettingsOld = 0x56
    dbiPowerSaving = 0x57
    dbiScalePercent = 0x58
    dbiPlaybackSpeedOld = 0x59
    dbiLanguagesKey = 0x5A
    dbiCallSettingsOld = 0x5B
    dbiCacheSettings = 0x5C
    dbiTxtDomainStringOld = 0x5D
    dbiApplicationSettings = 0x5E
    dbiDialogsFiltersOld = 0x5F
    dbiFallbackProductionConfig = 0x60
    dbiBackgroundKey = 0x61

    dbiEncryptedWithSalt = 333
    dbiEncrypted = 444

    dbiVersion = 666


def read_boolean(data: BytesIO) -> bool:
    return read_qt_int32(data) == 1


def read_settings_block(
    version, data: BytesIO, block_id: SettingsBlock
) -> Tuple[bool, int, bytes, str, dict]:
    if block_id == SettingsBlock.dbiAutoStart:
        return read_boolean(data)

    if block_id == SettingsBlock.dbiStartMinimized:
        return read_boolean(data)

    if block_id == SettingsBlock.dbiSongVolumeOld:
        return read_qt_int32(data) / 1e6

    if block_id == SettingsBlock.dbiSendToMenu:
        return read_boolean(data)

    if block_id == SettingsBlock.dbiSeenTrayTooltip:
        return read_boolean(data)

    if block_id == SettingsBlock.dbiAutoUpdate:
        return read_boolean(data)

    if block_id == SettingsBlock.dbiLastUpdateCheck:
        return read_qt_int32(data)

    if block_id == SettingsBlock.dbiScalePercent:
        return read_qt_int32(data)

    if block_id == SettingsBlock.dbiFallbackProductionConfig:

        def read_dc_options(data: BytesIO):
            minus_version = read_qt_int32(data)
            if minus_version < 0:
                version = -minus_version
            else:
                version = 0

            if version > 0:
                count = read_qt_int32(data)
            else:
                count = minus_version

            dc_options = []

            for _ in range(count):
                dc_option = {
                    "id": read_qt_int32(data),
                    "flags": read_qt_int32(data),
                    "port": read_qt_int32(data),
                    "ip": read_qt_byte_array(data).decode(),
                    "secret": read_qt_byte_array(data),
                }

                dc_options.append(dc_option)

            cdn_config = []

            if version > 1:
                count = read_qt_int32(data)
                for _ in range(count):
                    cfg = {
                        "dc_id": read_qt_int32(data),
                        "n": read_qt_byte_array(data),
                        "e": read_qt_byte_array(data),
                    }

                    cdn_config.append(cfg)

            return {"version": version, "dc": dc_options, "cdn": cdn_config}

        def read_fallback_config(data: BytesIO):
            return {
                "version": read_qt_int32(data),
                "environment": read_qt_int32(data),
                "dc_options": read_dc_options(BytesIO(read_qt_byte_array(data))),
                "chatSizeMax": read_qt_int32(data),
                "megagroupSizeMax": read_qt_int32(data),
                "forwardedCountMax": read_qt_int32(data),
                "onlineUpdatePeriod": read_qt_int32(data),
                "offlineBlurTimeout": read_qt_int32(data),
                "offlineIdleTimeout": read_qt_int32(data),
                "onlineFocusTimeout": read_qt_int32(data),
                "onlineCloudTimeout": read_qt_int32(data),
                "notifyCloudDelay": read_qt_int32(data),
                "notifyDefaultDelay": read_qt_int32(data),
                "savedGifsLimit": read_qt_int32(data),  # legacy
                "editTimeLimit": read_qt_int32(data),
                "revokeTimeLimit": read_qt_int32(data),
                "revokePrivateTimeLimit": read_qt_int32(data),
                "revokePrivateInbox": read_qt_int32(data),
                "stickersRecentLimit": read_qt_int32(data),
                "stickersFavedLimit": read_qt_int32(data),  # legacy
                "pinnedDialogsCountMax": read_qt_int32(data),  # legacy
                "pinnedDialogsInFolderMax": read_qt_int32(data),  # legacy
                "internalLinksDomain": read_qt_utf8(data),
                "channelsReadMediaPeriod": read_qt_int32(data),
                "callReceiveTimeoutMs": read_qt_int32(data),
                "callRingTimeoutMs": read_qt_int32(data),
                "callConnectTimeoutMs": read_qt_int32(data),
                "callPacketTimeoutMs": read_qt_int32(data),
                "webFileDcId": read_qt_int32(data),
                "txtDomainString": read_qt_utf8(data),
                "phoneCallsEnabled": read_qt_int32(data),  # legacy
                "blockedMode": read_qt_int32(data),
                "captionLengthMax": read_qt_int32(data),
                "reactionDefaultEmoji": read_qt_utf8(data),
                "reactionDefaultCustom": read_qt_uint64(data),
            }

        return read_fallback_config(BytesIO(read_qt_byte_array(data)))

    if block_id == SettingsBlock.dbiApplicationSettings:
        return read_qt_byte_array(data)

    if block_id == SettingsBlock.dbiDialogLastPath:
        return read_qt_utf8(data)

    if block_id == SettingsBlock.dbiPowerSaving:
        return read_qt_int32(data)

    if block_id == SettingsBlock.dbiThemeKey:
        return {
            "day": read_qt_uint64(data),
            "night": read_qt_uint64(data),
            "night_mode": read_boolean(data),
        }

    if block_id == SettingsBlock.dbiBackgroundKey:
        return {"day": read_qt_uint64(data), "night": read_qt_uint64(data)}

    if block_id == SettingsBlock.dbiTileBackground:
        return {"day": read_qt_int32(data), "night": read_qt_int32(data)}

    if block_id == SettingsBlock.dbiLangPackKey:
        return read_qt_uint64(data)

    if block_id == SettingsBlock.dbiMtpAuthorization:
        return read_qt_byte_array(data)

    if block_id == SettingsBlock.dbiLanguagesKey:
        return read_qt_uint64(data)

    raise SettingsReadException(f"Unnown block ID while reading settings: {block_id}")


class IncorrectBlockDataType(Exception):
    pass


def _ensure_correct_block_data_type(d):
    if any(isinstance(d, c) for c in (int, float, str, bytes)):
        return

    if isinstance(d, dict):
        for k, v in d.items():
            assert isinstance(k, str)
            _ensure_correct_block_data_type(v)
        return

    if isinstance(d, list):
        for v in d:
            _ensure_correct_block_data_type(v)
        return

    raise IncorrectBlockDataType(type(d))


def read_settings_blocks(version, data: BytesIO) -> Dict[SettingsBlock, Any]:
    blocks = {}

    try:
        while True:
            block_id = SettingsBlock(read_qt_int32(data))
            block_data = read_settings_block(version, data, block_id)
            _ensure_correct_block_data_type(block_data)
            blocks[block_id] = block_data
    except StopIteration:
        pass

    return blocks
