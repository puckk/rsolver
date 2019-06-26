# Rsolver

## Installation

Requeriments:

```
sudo apt-get install libmpfr-dev libmpc-dev
```



## ¿Cómo funciona?

Herramienta automática para atacar claves RSA débiles, con múltiples ataques y la selección del ataque óptimo para los datos ingresados.


```
usage: rsolver.py [-h] [--publickey PEM] [--inputfile FILE]
                  [--partialkey PARTIALKEY] [--partialkeyfile PARTIALKEYFILE]
                  [-p P] [-q Q] [-n N] [-e E] [-f PHI] [-c C]
                  [-c64file C64FILE] [--cfile CRYPTFILE] [-d D] [-dp DP]
                  [-dq DQ] [-qinv QINV] [--debug DEBUG] [--timeout TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit

Input Info:
  --publickey PEM       Input a Public key in PEM format
  --inputfile FILE      Input data (n,c,e or something) in decimals in text
                        file
  --partialkey PARTIALKEY, -pk PARTIALKEY
                        Input base64 priv key filling with * the first or last
                        character
  --partialkeyfile PARTIALKEYFILE, -pkf PARTIALKEYFILE
                        Filepath with base64 priv key filling with * the first
                        or last character
  -p P                  Input p value in decimal
  -q Q                  Input q value in decimal
  -n N                  Input n value in decimal
  -e E                  Input e value in decimal
  -f PHI                Input phi value in decimal
  -c C                  Input c value in decimal
  -c64file C64FILE      Input crypted file in base64
  --cfile CRYPTFILE, -x CRYPTFILE
                        Input encrypted/s file/s
  -d D                  Input d value in decimal
  -dp DP                Input dp value in decimal
  -dq DQ                Input dq value in decimal
  -qinv QINV            Input qinv value in decimal

Debug:
  --debug DEBUG         Debug mode
  --timeout TIMEOUT     Timeout for each script, default 120segs
```
 



## Ejemplos


1) **Send inputs by arguments**

Se pueden enviar los datos por argumentos, en decimal o en hexa (empezando con 0x)
```
python3 rsolver.py -n 9637828843823500407917687664441327784714605952794831018467094508166140790258515855681653788687192363262499178812675284846293988948568322307302995971433129 -e 65537 -c 0xe366a9aac8c1ca6652d71c80ded37b8e54d5c8f9599a59bdaa8ddac2ce4fc880b990094068ee5ba8ed53b849a73584a905e72e59d0f62fecdbccd10ce71c208
```


2) **Enviar más de un input como argumento**

Enviar varios exponentes públicos, separar por coma el argumento

```
python3 rsolver.py -e 11,41,67623079903,5161910578063,175238643578591220695210061216092361657427152135258210375005373467710731238260448371371798471959129039441888531548193154205671 -n 9247606623523847772698953161616455664821867183571218056970099751301682205123115716089486799837447397925308887976775994817175994945760278197527909621793469 -c 7117565509436551004326380884878672285722722211683863300406979545670706419248965442464045826652880670654603049188012705474321735863639519103720255725251120 --timeout 3
```


3) **Enviar un archivo con los datos**

Si los datos son muy grandes para mandar cómo parámetro, se pueden enviar un archivo con los parámetros 

*text file in examples/6.test*
```
N=0x1564aade6f1b9f169dcc94c9787411984cd3878bcd6236c5ce00b4aad6ca7cb0ca8a0334d9fe0726f8b057c4412cfbff75967a91a370a1c1bd185212d46b581676cf750c05bbd349d3586e78b33477a9254f6155576573911d2356931b98fe4fec387da3e9680053e95a4709934289dc0bc5cdc2aa97ce62a6ca6ba25fca6ae38c0b9b55c16be0982b596ef929b7c71da3783c1f20557e4803de7d2a91b5a6e85df64249f48b4cf32aec01c12d3e88e014579982ecd046042af370045f09678c9029f8fc38ebaea564c29115e19c7030f245ebb2130cbf9dc1c340e2cf17a625376ca52ad8163cfb2e33b6ecaf55353bc1ff19f8f4dc7551dc5ba36235af9758b
e=0x10001
phi=0x1564aade6f1b9f169dcc94c9787411984cd3878bcd6236c5ce00b4aad6ca7cb0ca8a0334d9fe0726f8b057c4412cfbff75967a91a370a1c1bd185212d46b581676cf750c05bbd349d3586e78b33477a9254f6155576573911d2356931b98fe4fec387da3e9680053e95a4709934289dc0bc5cdc2aa97ce62a6ca6ba25fca6ae366e86eed95d330ffad22705d24e20f9806ce501dda9768d860c8da465370fc70757227e729b9171b9402ead8275bf55d42000d51e16133fec3ba7393b1ced5024ab3e86b79b95ad061828861ebb71d35309559a179c6be8697f8a4f314c9e94c37cbbb46cef5879131958333897532fea4c4ecd24234d4260f54c4e37cb2db1a0
d=0x12314d6d6327261ee18a7c6ce8562c304c05069bc8c8e0b34e0023a3b48cf5849278d3493aa86004b02fa6336b098a3330180b9b9655cdf927896b22402a18fae186828efac14368e0a5af2c4d992cb956d52e7c9899d9b16a0a07318aa28c8202ebf74c50ccf49a6733327dde111393611f915f1e1b82933a2ba164aff93ef4ab2ab64aacc2b0447d437032858f089bcc0ddeebc45c45f8dc357209a423cd49055752bfae278c93134777d6e181be22d4619ef226abb6bfcc4adec696cac131f5bd10c574fa3f543dd7f78aee1d0665992f28cdbcf55a48b32beb7a1c0fa8a9fc38f0c5c271e21b83031653d96d25348f8237b28642ceb69f0b0374413308481
c=0x126c24e146ae36d203bef21fcd88fdeefff50375434f64052c5473ed2d5d2e7ac376707d76601840c6aa9af27df6845733b9e53982a8f8119c455c9c3d5df1488721194a8392b8a97ce6e783e4ca3b715918041465bb2132a1d22f5ae29dd2526093aa505fcb689d8df5780fa1748ea4d632caed82ca923758eb60c3947d2261c17f3a19d276c2054b6bf87dcd0c46acf79bff2947e1294a6131a7d8c786bed4a1c0b92a4dd457e54df577fb625ee394ea92b992a2c22e3603bf4568b53cceb451e5daca52c4e7bea7f20dd9075ccfd0af97f931c0703ba8d1a7e00bb010437bb4397ae802750875ae19297a7d8e1a0a367a2d6d9dd03a47d404b36d7defe8469
```

```
python3 rsolver.py --inputfile examples/6.test
```


4) **Partial private key**

EJEMPLO 1:

Supongase que usted tiene el archivo con la clave privada parcial,
```
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAMSwf+/I42wFwNpDQiGuv0fb9w5Ria2JJAjzrYEYKp4HAKB8nXxm
yGx6OWAhI+4PYFYT3pf95J/mg5buCvP19fMCAwEAAQJAKuxRnyR57PL8eSVAY1Vd
TPNF4QwOPZ62DHYRISEC++UtRemqE1eBPkRgswiJ91+r9y8EnVw/SvL4GYQmeovS
sQIhAOq8Heinxe4udriNOd35SgJV9e87YglCCIfCoAirR0qtAiEA1oIMcKaiRiUj
2S/Q4YFTNySdT+fH16huoSQrEapD9x8*********************************
****************************************************************
********************************************
-----END RSA PRIVATE KEY-----
```

Entonces usted puede explotarla con el parámetro -pk, y seteando un asterisco al principio o al final de la key (para setear si son los primeros bytes o los ltimos los que se tienen)
```
python3 rsolver.py -pk MIIBOwIBAAJBAMSwf+/I42wFwNpDQiGuv0fb9w5Ria2JJAjzrYEYKp4HAKB8nXxmyGx6OWAhI+4PYFYT3pf95J/mg5buCvP19fMCAwEAAQJAKuxRnyR57PL8eSVAY1VdTPNF4QwOPZ62DHYRISEC++UtRemqE1eBPkRgswiJ9+r9y8EnVw/SvL4GYQmeovSsQIhAOq8Heinxe4udriNOd35SgJV9e87YglCCIfCoAirR0qtAiEA1oIMcKaiRiUj2S/Q4YFTNySdT+fH16huoSQrEapD9x8*
```

EJEMPLO 2:

Desde un archivo con -pkf

*examples/25.test*

```
MIIBOwIBAAJBAMSwf+/I42wFwNpDQiGuv0fb9w5Ria2JJAjzrYEYKp4HAKB8nXxmyGx6OWAhI+4PYFYT3pf95J/mg5buCvP19fMCAwEAAQJAKuxRnyR57PL8eSVAY1VdTPNF4QwOPZ62DHYRISEC++UtRemqE1eBPkRgswiJ9+r9y8EnVw/SvL4GYQmeovSsQIhAOq8Heinxe4udriNOd35SgJV9e87YglCCIfCoAirR0qtAiEA1oIMcKaiRiUj2S/Q4YFTNySdT+fH16huoSQrEapD9x8*
```

```
python3 rsolver.py -pkf examples/25.test
```

EJEMPLO 3:

En cambio, si usted tiene los últimos bytes:
```
python3 rsolver.py -pk *Os9mhOQRdqW2cwVrnNI72DLcAXpXUJ1HGwJBANWiJcDUGxZpnERxVw7s0913WXNtV4GqdxCzG0pG5EHThtoTRbyX0aqRP4U/hQ9tRoSoDmBn+3HPITsnbCy67VkCQBM4xZPTtUKM6Xi+16VTUnFVs9E4rqwIQCDAxn9UuVMBXlX2Cl0xOGUF4C5hItrX2woF7LVS5EizR63CyRcPovMCQQDVyNbcWD7N88MhZjujKuSrHJot7WcCaRmTGEIJ6TkU8NWt9BVjR4jVkZ2EqNd0KZWdQPukeynPcLlDEkIXyaQx --cfile examples/x/flag.enc -e 65537
```
