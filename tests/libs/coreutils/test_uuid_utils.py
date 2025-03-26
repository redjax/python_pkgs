import pytest
import uuid
from core_utils.uuid_utils import gen_uuid, trim_uuid, first_n_chars, get_rand_uuid
from core_utils.uuid_utils import UUIDLength

from .fixtures import uuid_lengths

## Test gen_uuid function
def test_gen_uuid():
    ## Test default behavior (returns a UUID object)
    result = gen_uuid()
    assert isinstance(result, uuid.UUID)

    ## Test as_hex=True (returns a hex string)
    result_hex = gen_uuid(as_hex=True)
    assert isinstance(result_hex, str)
    assert len(result_hex) == 32  # Hex UUID has 32 characters
    assert "-" not in result_hex

## Test trim_uuid function
def test_trim_uuid(uuid_lengths: UUIDLength):
    test_uuid = str(uuid.uuid4())  # Generate a standard UUID string

    ## Test trimming 4 characters from the end
    trimmed = trim_uuid(trim=4, in_uuid=test_uuid)
    assert len(trimmed) == uuid_lengths.standard - 4

    ## Test trimming with as_hex=True
    trimmed_hex = trim_uuid(trim=4, in_uuid=test_uuid, as_hex=True)
    assert len(trimmed_hex) == uuid_lengths.hex - 4

    ## Test invalid trim value (negative)
    with pytest.raises(ValueError):
        trim_uuid(trim=-1, in_uuid=test_uuid)

    ## Test invalid trim value (too large)
    with pytest.raises(ValueError):
        trim_uuid(trim=uuid_lengths.standard + 1, in_uuid=test_uuid)

## Test first_n_chars function
def test_first_n_chars(uuid_lengths):
    ## Generate a standard UUID string
    test_uuid = str(uuid.uuid4())

    ## Test returning the first 8 characters
    first_n = first_n_chars(first_n=8, in_uuid=test_uuid)
    assert len(first_n) == 8

    ## Test returning the first 8 characters with as_hex=True
    first_n_hex = first_n_chars(first_n=8, in_uuid=test_uuid, as_hex=True)
    assert len(first_n_hex) == 8

    ## Test invalid first_n value (negative)
    with pytest.raises(ValueError):
        first_n_chars(first_n=-1, in_uuid=test_uuid)

    ## Test invalid first_n value (too large)
    with pytest.raises(ValueError):
        first_n_chars(first_n=uuid_lengths.standard + 1, in_uuid=test_uuid)

## Test get_rand_uuid function
def test_get_rand_uuid():
    ## Test default behavior (returns a full UUID string)
    result = get_rand_uuid()
    assert isinstance(result, str)
    assert len(result) == 36

    ## Test as_hex=True (returns a hex string)
    result_hex = get_rand_uuid(as_hex=True)
    assert isinstance(result_hex, str)
    assert len(result_hex) == 32

    ## Test trimming characters from the end
    trimmed = get_rand_uuid(trim=4)
    assert len(trimmed) == 36 - 4

    ## Test returning the first n characters
    first_n = get_rand_uuid(characters=8)
    assert len(first_n) == 8

    ## Test invalid combination of trim and characters
    with pytest.raises(ValueError):
        get_rand_uuid(trim=4, characters=8)

## Edge case tests for get_rand_uuid function
def test_get_rand_uuid_invalid_inputs():
    ## Invalid trim value (negative)
    with pytest.raises(ValueError):
        get_rand_uuid(trim=-1)

    ## Invalid characters value (negative)
    with pytest.raises(ValueError):
        get_rand_uuid(characters=-1)


@pytest.mark.xfail(reason="UUID version not yet implemented")
def test_gen_uuid_with_version():
    result = gen_uuid(version=4)
    assert result.version == 4

@pytest.mark.xfail(reason="Trim larger than UUID length not properly handled")
def test_trim_uuid_excessive_trim(uuid_lengths):
    test_uuid = str(uuid.uuid4())
    trimmed = trim_uuid(trim=uuid_lengths.standard + 1, in_uuid=test_uuid)
    assert trimmed == ""

@pytest.mark.xfail(reason="Non-integer input for first_n not yet supported")
def test_first_n_chars_non_integer():
    test_uuid = str(uuid.uuid4())
    result = first_n_chars(first_n="8", in_uuid=test_uuid)
    assert len(result) == 8

@pytest.mark.xfail(reason="Handling of non-UUID input strings not implemented")
def test_get_rand_uuid_non_uuid_input():
    result = get_rand_uuid(in_uuid="not-a-uuid")
    assert isinstance(result, str)

@pytest.mark.xfail(reason="Concurrent UUID generation not yet optimized")
def test_concurrent_uuid_generation():
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        uuids = list(executor.map(gen_uuid, range(1000)))
    assert len(set(uuids)) == 1000

@pytest.mark.xfail(reason="UUID namespacing not implemented")
def test_uuid_namespace():
    namespace = uuid.NAMESPACE_DNS
    name = "example.com"
    result = gen_uuid(namespace=namespace, name=name)
    assert isinstance(result, uuid.UUID)
