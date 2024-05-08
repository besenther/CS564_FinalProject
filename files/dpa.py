import h5py
import binascii



def xor(b1, b2):
    return bytes(a^b for a,b in zip(b1,b2))


data = h5py.File("aes_decrypt_powertraces_test_target.hdf5")
powertrace_0 = data['data_000000']


key = binascii.unhexlify(powertrace_0.attrs['dut_key'])
print(key)
c = binascii.unhexlify(powertrace_0.attrs['dut_input'])
print(key)
pt = binascii.unhexlify(powertrace_0.attrs['dut_output'])
print(key)


res = xor(pt,c)
r10 = xor(res,key)

print(r10.hex())