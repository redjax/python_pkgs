# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "coreutils-lib",
#     "loguru",
# ]
#
# [tool.uv.sources]
# coreutils-lib = { path = "../../libs/coreutils-lib" }
# pandas-lib = { path = "../../libs/pandas-lib" }
# ///

from loguru import logger as log

from core_utils import path_utils, hash_utils, list_utils, time_utils, uuid_utils

if __name__ == "__main__":
    log.info("core_utils sandbox")

    sanitized_filename: str = path_utils.sanitize_filename("C:\\test\\path?name.txt")
    log.info(f"Santized filename: {sanitized_filename}")
    
    str_hash = hash_utils.get_hash_from_str("This is a test input string!")
    log.info(f"Hashed string: {str_hash}")
    
    og_list: list[str] = ["This is the first string", "This is the second string", "This is the third string"]
    shuffled_list = list_utils.shuffle_list(og_list)
    log.info(f"Shuffled list: {shuffled_list}")
    
    random_index = list_utils.get_random_index(og_list)
    log.info(f"Random index: {random_index}, item: {og_list[random_index]}")
    
    random_item = list_utils.get_random_item(og_list)
    log.info(f"Random item: {random_item}")
    
    ts = time_utils.get_ts()
    log.info(f"Timestamp: {ts}")
    
    time_24h = time_utils.datetime_as_str(ts=ts, format=time_utils.TIME_FMT_24H)
    time_12h = time_utils.datetime_as_str(ts=ts, format=time_utils.TIME_FMT_12H)
    log.info(f"Timestamp: {time_24h} (24h), {time_12h} (12h)")
    
    _uuid = uuid_utils.gen_uuid()
    _uuid_hex = uuid_utils.gen_uuid(as_hex=True)
    log.info(f"UUID: {_uuid}")
    log.info(f"UUID (hex): {_uuid_hex}")
    
    rand_uuid = uuid_utils.get_rand_uuid()
    rand_uuid_trim5 = uuid_utils.get_rand_uuid(trim=5)
    rand_uuid_14chars = uuid_utils.get_rand_uuid(characters=14)
    rand_uuid_trim8_str = uuid_utils.get_rand_uuid(trim=8, as_str=True)
    rand_uuid_trimmed = uuid_utils.first_n_chars(first_n=18, in_uuid=rand_uuid)
    rand_uuid_trimmed2 = uuid_utils.trim_uuid(trim=6, in_uuid=rand_uuid)
    
    log.info(f"Random UUID: {rand_uuid}")
    log.info(f"Random UUID (trimmed): {rand_uuid_trim5}")
    log.info(f"Random UUID (first 14 chars): {rand_uuid_14chars}")
    log.info(f"Random UUID (trimmed, str): {rand_uuid_trim8_str}")
    log.info(f"Random UUID (trimmed with first_n_chars()): {rand_uuid_trimmed}")
    log.info(f"Random UUID (trimmed with trim_uuid()): {rand_uuid_trimmed2}")
