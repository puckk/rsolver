import unittest
import subprocess
from base64 import b64encode
from collections import OrderedDict

class TestRsolver(unittest.TestCase):
    tests={
            "00": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/8.test", "path":"output_01/plaintext_cdn","solution":"IceCTF{falls_apart_so_easily_and_reassembled_so_crudely}", "md5": "05177bc720d2b7a6be6e62f1c991caf6"},
           "01": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/2.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"actf{rsa_is_reallllly_fun!!!!!!}", "md5": "690db329b716699cc2081ae693f299d8"},
           "02": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/3.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"easyctf{keblftftzibatdsqmqotemmty}", "md5":"0199baead5144c92d0464a403ae469cc"},
           "03": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/5.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"CTF{c0n6r47zzz_y0u_f0und_0ur_h1dd3n_w13n3r!!}","md5": "abff64b4c269d71c86bdcb5089f1ae1a"},
           "04": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/6.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"IceCTF{rsa_is_awesome_when_used_correctly_but_horrible_when_not}", "md5":"6b5eeb2b5bdfdab271f65ac3edf6bbe7"},
           "05": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/7.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"IceCTF{next_time_check_your_keys_arent_factorable}", "md5": "2399fea05b0c1a80c2dd1b2feef50790" },
           "06": {"command":"python3 rsolver.py --timeout 15 --inputfile examples/1.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"easyctf{4b8xofjwvy4rqkbuba}", "md5":"ca17ef997678f48bcb0a8ef584bffc50"},
           "07": {"command":"python3 rsolver.py  --c64file examples/9/flag.enc --publickey examples/9/public.key --timeout 5", "path":"$(ls | grep output_ | tail -n 1)/plaintext_oaep","solution":"EKO{classic_rsa_challenge_is_boring_but_necessary}", "md5": "d42c8d46be8db057d1a7933cf4d46812"},
           "08": {"command":"python3 rsolver.py --inputfile examples/10.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"NTEzMjU2MzI3MTA4MDgzNzE3Mjg4MzE2OTU4MTc4MTEwNTI1NzE4OTEyMTM0MDMzNTY3Mjc3Njc2NTI1MjYxMjI5MjExMzE0MDE1ODk=", "md5":"afc3e85feda4adfa744620fa3df3e923"},
           "09": {"command":"python3 rsolver.py --inputfile examples/12.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"d4rk{s1mpl3_rsa_n0t_th1s_34sy_next_time}c0de", "md5": "85b0ce932fb9c646e0fc46d999a51b0b"},
           "10": {"command":"python3 rsolver.py --timeout 5 --inputfile examples/13.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"d4rk{1_70ld_y0u_th15_would_8e_more_difficult}c0de", "md5":"e7980c13a42b939fd9f6aecde46a13d8"},
           "11": {"command":"python3 rsolver.py --timeout 5 --inputfile examples/15.test", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"inctf{w13n3r's_4774ck_s0lv3d_17_4ll_r1gh7?}", "md5": "b880d928473360c9c6388b899622257c"},
           "12": {"command":"python3 rsolver.py --publickey examples/16/PublicKey1.pem --cfile examples/16/ciphertext1.txt", "path":"$(ls | grep output_ | tail -n 1)/plaintext*","solution":"-", "md5":"00d4314e27282ccf478263a8d40cda89"},
           "13": {"command":"python3 rsolver.py --publickey examples/16/PublicKey2.pem --cfile examples/16/ciphertext2.txt", "path":"$(ls | grep output_ | tail -n 1)/plaintext*","solution":"-", "md5":"48258a052afd81655312fed20e0d17b1"},
           "14": {"command":"python3 rsolver.py --publickey examples/16/PublicKey3.pem --cfile examples/16/ciphertext3.txt", "path":"$(ls | grep output_ | tail -n 1)/plaintext*","solution":"-", "md5":"08402bdbe9c678acc9b7fdb32497a972"},
           "15": {"command":"python3 rsolver.py -pk *Os9mhOQRdqW2cwVrnNI72DLcAXpXUJ1HGwJBANWiJcDUGxZpnERxVw7s0913WXNtV4GqdxCzG0pG5EHThtoTRbyX0aqRP4U/hQ9tRoSoDmBn+3HPITsnbCy67VkCQBM4xZPTtUKM6Xi+16VTUnFVs9E4rqwIQCDAxn9UuVMBXlX2Cl0xOGUF4C5hItrX2woF7LVS5EizR63CyRcPovMCQQDVyNbcWD7N88MhZjujKuSrHJot7WcCaRmTGEIJ6TkU8NWt9BVjR4jVkZ2EqNd0KZWdQPukeynPcLlDEkIXyaQx  -e 65537 --cfile examples/x/flag.enc", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"-", "md5":"aebe59840c1b4eab2be599fd291f086d"},
           "16": {"command":"python3 rsolver.py --inputfile examples/19.test  --timeout 5", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"-", "md5":"7dbd48237be8291ce05ddb45c45cf02a"},
           "17": {"command":"python3 rsolver.py --inputfile examples/21.test  --timeout 6", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"-", "md5":"8ac8be14a5e1df2fb90b42e7a06a89ee"},
           "18": {"command":"python3 rsolver.py --inputfile examples/22.test --timeout 3", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"-", "md5":"4b91ce46f90172c05f93bf1650d28017"},
           "19": {"command":"python3 rsolver.py --inputfile examples/23.test --timeout 5", "path":"$(ls | grep output_ | tail -n 1)/plaintext_cdn","solution":"-", "md5":"809c6dada3e27a14f1d17eaa2a7e4208"},
           "20": {"command":"python3 rsolver.py --c64file examples/27/cipher.text --publickey examples/27/pubkey.pem", "path":"$(ls | grep output_ | tail -n 1)/plaintext","solution":"-", "md5":"cbc92c4e7eaf4ecf238c1687a0c6740b"},
           "21": {"command":"python3 rsolver.py -e 0xf70b3bd74801a25eccbde24e01b077677e298391d4197b099a6f961244f04314da7de144dd69a8aa84686bf4ddbd14a6344bbc315218dbbaf29490a44e42e5c4a2a4e76b8101a5ca82351c07b4cfd4e08038c8d5573a827b227bce515b70866724718ec2ac03359614cdf43dd88f1ac7ee453917975a13c019e620e531207692224009c75eaef11e130f8e54cce31e86c84e9366219ae5c250853be145ea87dcf37aa7ece0a994195885e31ebcd8fe742df1cd1370c95b6684ab6c37e84762193c27dd34c3cf3f5e69957b8338f9143a0052c9381d9e2ecb9ef504c954b453f57632705ed44b28a4b5cbe61368e485da6af2dfc901e45868cdd5006913f338a3 -n 0x0207a7df9d173f5969ad16dc318496b36be39fe581207e6ea318d3bfbe22c8b485600ba9811a78decc6d5aab79a1c2c491eb6d4f39820657b6686391b85474172ae504f48f02f7ee3a2ab31fce1cf9c22f40e919965c7f67a8acbfa11ee4e7e2f3217bc9a054587500424d0806c0e759081651f6e406a9a642de6e8e131cb644a12e46573bd8246dc5e067d2a4f176fef6eec445bfa9db888a35257376e67109faabe39b0cf8afe2ca123da8314d09f2404922fc4116d682a4bdaeecb73f59c49db7fa12a7fc5c981454925c94e0b5472e02d924dad62c260066e07c7d3b1089d5475c2c066b7f94553c75e856e3a2a773c6c24d5ba64055eb8fea3e57b06b04a3 --timeout 6", "path":"$(ls | grep output_ | tail -n 1)/privateKey.pem","solution":"-", "md5":"47a6e044d22242f8f5ac3b371d0debaf"},
           "22": {"command":"python3 rsolver.py -blind -n 456378902858290907415273676326459758501863587455889046415299414290812776158851091008643992243505529957417209835882169153356466939122622249355759661863573516345589069208441886191855002128064647429111920432377907516007825359999 -e 65537 -c 41662410494900335978865720133929900027297481493143223026704112339997247425350599249812554512606167456298217619549359408254657263874918458518753744624966096201608819511858664268685529336163181156329400702800322067190861310616 --timeout 5 -ucp 1458414996286361336171022694278618963923904557163518886908519150023343172644758356895532151523030", "path":"$(ls | grep output_ | tail -n 1)/plaintext_blind","solution":"Well done! The flag is S1d3Ch4nn3l4tt4ck", "md5": "80cdc9a5d5e93afca4ac2acb6195fe77"},



#           "16": {"command":"python3 rsolver.py --inputfile examples/18.test --timeout 99999", "path":"output_17/PLAINTEXTE","solution":"-", "md5":"aebe59840c1b4eab2be599fd291f086d"},










    }

    def test_upper(self):
        subprocess.check_output("rm -rf output_*",shell=True)

        for i in sorted(OrderedDict(sorted(self.tests.items()))):
            print (i)
            comando=self.tests[i]["command"]
            path=self.tests[i]["path"]
            sol=self.tests[i]["solution"]
            hash=self.tests[i]["md5"]
#            print ("A")
            subprocess.check_output(comando,shell=True)
#            print ("B")
            t="md5sum {} | cut -d \" \" -f 1 | tr -d '\n'".format(path)
            self.assertEqual (subprocess.check_output(t,shell=True).decode("utf-8"),hash, msg="Failed command {}\n\n\n{}".format(comando,t))



if __name__ == '__main__':
    unittest.main()
