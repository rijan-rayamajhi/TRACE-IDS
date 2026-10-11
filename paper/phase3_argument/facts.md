## Table 1 datasets
          dataset  key   flows  features  attack_flows  attack_rate  attack_families  attack_categories                    sampling
NF-CICIDS2018-v3  cic 2011553        45        260748       0.1296               14                  6               10.0% uniform
 NF-UNSW-NB15-v3 unsw 2365424        45        127693       0.0540                9                  9                   all flows
   NF-ToN-IoT-v3  ton 2064020        45        805024       0.3900                9                  8                7.5% uniform
   NF-BoT-IoT-v3  bot 2077807        45       2025818       0.9750                4                  4 all benign + attacks at 12%

## E1 (RF, CIC<->UNSW) F1 mean±std by mode/features/k
                         f1_mean                              
mode                   source+k source+k-weighted target-only
direction features k                                         
cic->unsw -TTL     0      0.000               NaN         NaN
                   1      0.074             0.062       0.162
                   5      0.542             0.667       0.500
                   10     0.635             0.743       0.596
                   50     0.912             0.923       0.917
                   100    0.969             0.960       0.955
                   500    0.989             0.989       0.989
          all      0      0.000               NaN         NaN
                   1      0.107             0.130       0.154
                   5      0.700             0.754       0.697
                   10     0.775             0.832       0.811
                   50     0.935             0.969       0.976
                   100    0.982             0.982       0.986
                   500    0.994             0.995       0.996
unsw->cic -TTL     0      0.065               NaN         NaN
                   1      0.344             0.299       0.302
                   5      0.426             0.459       0.411
                   10     0.573             0.614       0.539
                   50     0.868             0.835       0.839
                   100    0.922             0.914       0.911
                   500    0.935             0.935       0.933
          all      0      0.235               NaN         NaN
                   1      0.262             0.266       0.297
                   5      0.390             0.407       0.410
                   10     0.530             0.531       0.555
                   50     0.871             0.827       0.842
                   100    0.923             0.921       0.917
                   500    0.939             0.936       0.936

E1 FPR at k=1:
 mode                source+k  source+k-weighted  target-only
direction features                                          
cic->unsw -TTL         0.019              0.029        0.409
          all          0.005              0.000        0.400
unsw->cic -TTL         0.231              0.215        0.486
          all          0.365              0.339        0.451

## E3 per-domain: 540 tests {'no diff': 353, 'hurt': 153, 'help': 34} | Holm: {'no diff': 540} | median dF1 -0.0114 mean -0.0385 | min p 0.0020
by method
 verdict   help  hurt  no diff
method                       
finetune    10    72       98
iw           9    41      130
pooled      15    40      125
by model
 verdict  help  hurt  no diff
model                       
GBT         4    32      144
MLP        19    54      107
RF         11    67      102
by k
 verdict  help  hurt  no diff
k                           
1           9    27       72
5           3    31       74
10          4    35       69
50          8    31       69
100        10    29       69
by pair
 verdict    help  hurt  no diff
direction                     
bot->cic      3    16       26
bot->ton      0     8       37
bot->unsw     1    26       18
cic->bot      5    24       16
cic->ton      1    11       33
cic->unsw     0    11       34
ton->bot      6    14       25
ton->cic      9     5       31
ton->unsw     2     9       34
unsw->bot     5    10       30
unsw->cic     0    14       31
unsw->ton     2     5       38
E2 subset (CIC<->UNSW, 90 tests): {'no diff': 65, 'hurt': 25}
zero-shot best bacc per pair
 direction
bot->cic     0.662
bot->ton     0.605
bot->unsw    0.561
cic->bot     0.501
cic->ton     0.502
cic->unsw    0.500
ton->bot     0.671
ton->cic     0.509
ton->unsw    0.498
unsw->bot    0.710
unsw->cic    0.512
unsw->ton    0.662
target-only bacc (k=1,5,10)
 direction     1     5    10
 bot->cic 0.610 0.731 0.823
 bot->ton 0.570 0.773 0.781
bot->unsw 0.645 0.900 0.938
 cic->bot 0.636 0.821 0.857
 cic->ton 0.570 0.773 0.781
cic->unsw 0.645 0.900 0.938
 ton->bot 0.636 0.821 0.857
 ton->cic 0.610 0.731 0.823
ton->unsw 0.645 0.900 0.938
unsw->bot 0.636 0.821 0.857
unsw->cic 0.610 0.731 0.823
unsw->ton 0.570 0.773 0.781

## E3 shared: 540 tests {'no diff': 294, 'hurt': 205, 'help': 41} | Holm: {'no diff': 540} | median dF1 -0.0247 mean -0.0439 | min p 0.0020
by method
 verdict   help  hurt  no diff
method                       
finetune    12    73       95
iw          12    74       94
pooled      17    58      105
by model
 verdict  help  hurt  no diff
model                       
GBT        13    39      128
MLP        25    67       88
RF          3    99       78
by k
 verdict  help  hurt  no diff
k                           
1          11    28       69
5           6    37       65
10          5    35       68
50          8    56       44
100        11    49       48
by pair
 verdict    help  hurt  no diff
direction                     
bot->cic     14    16       15
bot->ton      1    22       22
bot->unsw     0    25       20
cic->bot      7    21       17
cic->ton      0    23       22
cic->unsw     0    18       27
ton->bot      6    23       16
ton->cic      0    18       27
ton->unsw     1    13       31
unsw->bot     9     3       33
unsw->cic     0    20       25
unsw->ton     3     3       39
E2 subset (CIC<->UNSW, 90 tests): {'no diff': 52, 'hurt': 38}
zero-shot best bacc per pair
 direction
bot->cic     0.760
bot->ton     0.681
bot->unsw    0.476
cic->bot     0.498
cic->ton     0.535
cic->unsw    0.500
ton->bot     0.526
ton->cic     0.553
ton->unsw    0.502
unsw->bot    0.689
unsw->cic    0.578
unsw->ton    0.742
target-only bacc (k=1,5,10)
 direction     1     5    10
 bot->cic 0.607 0.728 0.822
 bot->ton 0.567 0.772 0.777
bot->unsw 0.647 0.904 0.937
 cic->bot 0.646 0.822 0.860
 cic->ton 0.581 0.772 0.780
cic->unsw 0.645 0.900 0.936
 ton->bot 0.651 0.821 0.859
 ton->cic 0.607 0.727 0.822
ton->unsw 0.647 0.901 0.936
unsw->bot 0.654 0.820 0.856
unsw->cic 0.610 0.726 0.823
unsw->ton 0.568 0.772 0.779

## E4a Atif & Ali replication: best F1 / bal_acc per direction, features, test (max over scaling & model)
                              f1_mean  bal_acc_mean
direction features test                           
cic->unsw A        balanced    0.022         0.500
                   natural     0.013         0.500
          B        balanced    0.040         0.500
                   natural     0.016         0.500
          C        balanced    0.183         0.520
                   natural     0.096         0.521
          Cv2      balanced    0.196         0.527
                   natural     0.105         0.527
          all      balanced    0.040         0.500
                   natural     0.010         0.500
unsw->cic A        balanced    0.540         0.541
                   natural     0.234         0.542
          B        balanced    0.080         0.501
                   natural     0.057         0.501
          C        balanced    0.208         0.517
                   natural     0.133         0.517
          Cv2      balanced    0.250         0.506
                   natural     0.115         0.506
          all      balanced    0.509         0.552
                   natural     0.208         0.552

## E4b TAN-IDS 5% budget F1
 method           finetune  pooled  source-only  target-only
direction model                                            
cic->unsw GBT      0.9979  0.9988       0.0101       0.9996
          MLP      0.9980  0.9939       0.0120       0.9972
          RF       0.9976  0.9989       0.0000       0.9990
unsw->cic GBT      0.9136  0.9666       0.0631       0.9667
          MLP      0.9656  0.9565       0.1639       0.9594
          RF       0.9662  0.9636       0.1994       0.9638

## E5-B domain AUC (mean over seeds): min over pairs per subset/scaling
 subset          scaling
all             raw        0.9993
                zscore     1.0000
attack          raw        1.0000
                zscore     1.0000
benign          raw        0.9992
                zscore     1.0000
cat:backdoor    raw        1.0000
                zscore     1.0000
cat:bruteforce  raw        1.0000
                zscore     1.0000
cat:ddos        raw        1.0000
                zscore     1.0000
cat:dos         raw        0.9966
                zscore     0.9967
cat:scanning    raw        0.9994
                zscore     0.9996

## E5-A families summary columns: ['direction', 'category', 'in_source', 'model', 'method', 'k', 'recall', 'recall_std', 'n_test'] rows 1215

## E5 RF importance rank corr range: 0.253 - 0.828

## Ablation: features removed before AUC < thr (mean over seeds), raw
                  removed_to_<0.95  removed_to_<0.9  removed_to_<0.75  removed_to_<0.6
subset pair                                                                          
all    cic-bot               28.7             29.0              35.3             38.0
       cic-ton               21.3             24.0              35.0             38.0
       cic-unsw              38.7             39.7              41.3             44.0
       ton-bot               20.0             22.7              28.0             35.7
       unsw-bot              32.7             35.0              41.7             43.3
       unsw-ton              34.3             37.3              40.7             42.3
benign cic-bot               20.0             23.7              35.0             38.0
       cic-ton               21.0             22.3              33.0             38.0
       cic-unsw              37.3             39.3              40.7             44.0
       ton-bot               13.0             17.0              21.7             34.3
       unsw-bot              36.7             38.3              40.7             43.0
       unsw-ton              32.7             37.3              39.7             42.0
raw range removed_to_<0.9: {'min': 17.0, 'max': 39.7}
AUC after n removed (raw, mean over pairs&seeds)
 subset       all  benign
n_removed               
0          1.000   1.000
5          0.999   0.999
10         0.999   0.994
15         0.997   0.988
20         0.986   0.934
30         0.864   0.858

## Single-feature AUC>=0.99: raw 13 zscore 231 of 270
cic-unsw PROTOCOL: [{'raw': 0.565, 'zscore': 1.0}]
