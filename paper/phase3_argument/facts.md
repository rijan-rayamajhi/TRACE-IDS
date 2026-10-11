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
median dF1 by k: {1: -0.0147, 5: -0.0254, 10: -0.029, 50: -0.0032, 100: -0.0002}
E2 subset (CIC<->UNSW, 90 tests): {'no diff': 65, 'hurt': 25}
zero-shot per pair/model (f1, recall, fpr, bacc)
 direction model    f1  recall   fpr  bacc
 bot->cic   GBT 0.273   0.912 0.712 0.600
 bot->cic   MLP 0.311   0.921 0.596 0.662
 bot->cic    RF 0.230   1.000 1.000 0.500
 bot->ton   GBT 0.572   0.931 0.846 0.542
 bot->ton   MLP 0.579   0.755 0.546 0.605
 bot->ton    RF 0.561   0.998 0.999 0.499
bot->unsw   GBT 0.105   0.870 0.844 0.513
bot->unsw   MLP 0.116   0.954 0.832 0.561
bot->unsw    RF 0.103   0.997 0.991 0.503
 cic->bot   GBT 0.015   0.008 0.005 0.501
 cic->bot   MLP 0.334   0.206 0.612 0.297
 cic->bot    RF 0.000   0.000 0.000 0.500
 cic->ton   GBT 0.015   0.008 0.013 0.498
 cic->ton   MLP 0.358   0.334 0.330 0.502
 cic->ton    RF 0.000   0.000 0.000 0.500
cic->unsw   GBT 0.010   0.018 0.165 0.427
cic->unsw   MLP 0.012   0.045 0.327 0.359
cic->unsw    RF 0.000   0.000 0.000 0.500
 ton->bot   GBT 0.144   0.090 0.095 0.498
 ton->bot   MLP 0.538   0.386 0.045 0.671
 ton->bot    RF 0.031   0.017 0.158 0.429
 ton->cic   GBT 0.065   0.070 0.099 0.485
 ton->cic   MLP 0.162   0.313 0.396 0.458
 ton->cic    RF 0.034   0.020 0.001 0.509
ton->unsw   GBT 0.039   0.032 0.050 0.491
ton->unsw   MLP 0.062   0.194 0.313 0.440
ton->unsw    RF 0.000   0.000 0.004 0.498
unsw->bot   GBT 0.000   0.000 0.006 0.497
unsw->bot   MLP 0.725   0.576 0.156 0.710
unsw->bot    RF 0.060   0.043 0.121 0.461
unsw->cic   GBT 0.063   0.098 0.075 0.512
unsw->cic   MLP 0.164   0.282 0.305 0.488
unsw->cic    RF 0.199   0.473 0.457 0.508
unsw->ton   GBT 0.086   0.075 0.010 0.532
unsw->ton   MLP 0.373   0.281 0.065 0.608
unsw->ton    RF 0.481   0.389 0.066 0.662
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
median dF1 by k: {1: -0.026, 5: -0.0367, 10: -0.0328, 50: -0.0258, 100: -0.0173}
E2 subset (CIC<->UNSW, 90 tests): {'no diff': 52, 'hurt': 38}
zero-shot per pair/model (f1, recall, fpr, bacc)
 direction model    f1  recall   fpr  bacc
 bot->cic   GBT 0.468   0.738 0.217 0.760
 bot->cic   MLP 0.352   0.463 0.158 0.652
 bot->cic    RF 0.359   0.918 0.477 0.720
 bot->ton   GBT 0.570   0.815 0.674 0.570
 bot->ton   MLP 0.606   0.688 0.371 0.658
 bot->ton    RF 0.647   0.816 0.455 0.681
bot->unsw   GBT 0.081   0.244 0.317 0.464
bot->unsw   MLP 0.081   0.305 0.378 0.464
bot->unsw    RF 0.095   0.743 0.792 0.476
 cic->bot   GBT 0.119   0.065 0.130 0.468
 cic->bot   MLP 0.215   0.126 0.608 0.259
 cic->bot    RF 0.117   0.063 0.068 0.498
 cic->ton   GBT 0.275   0.194 0.125 0.535
 cic->ton   MLP 0.356   0.319 0.292 0.514
 cic->ton    RF 0.111   0.071 0.134 0.469
cic->unsw   GBT 0.009   0.026 0.283 0.372
cic->unsw   MLP 0.054   0.194 0.369 0.413
cic->unsw    RF 0.002   0.001 0.001 0.500
 ton->bot   GBT 0.173   0.104 0.095 0.505
 ton->bot   MLP 0.247   0.162 0.110 0.526
 ton->bot    RF 0.105   0.057 0.082 0.488
 ton->cic   GBT 0.059   0.062 0.137 0.462
 ton->cic   MLP 0.163   0.337 0.420 0.459
 ton->cic    RF 0.220   0.208 0.101 0.553
ton->unsw   GBT 0.028   0.051 0.142 0.455
ton->unsw   MLP 0.062   0.262 0.417 0.422
ton->unsw    RF 0.009   0.004 0.001 0.502
unsw->bot   GBT 0.084   0.046 0.273 0.387
unsw->bot   MLP 0.756   0.619 0.241 0.689
unsw->bot    RF 0.712   0.592 0.227 0.683
unsw->cic   GBT 0.179   0.223 0.120 0.552
unsw->cic   MLP 0.263   0.680 0.524 0.578
unsw->cic    RF 0.210   0.543 0.531 0.506
unsw->ton   GBT 0.162   0.149 0.318 0.415
unsw->ton   MLP 0.675   0.622 0.138 0.742
unsw->ton    RF 0.574   0.496 0.161 0.668
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

## IW effective sample size (fraction of source), per-domain: min 0.0503 max 0.6784 median 0.3426

## IW effective sample size (fraction of source), shared: min 0.0009 max 0.0380 median 0.0084

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

## E4b TAN-IDS 5% budget F1 (per-domain)
 method           finetune  pooled  source-only  target-only
direction model                                            
cic->unsw GBT      0.9979  0.9988       0.0101       0.9996
          MLP      0.9980  0.9939       0.0120       0.9972
          RF       0.9976  0.9989       0.0000       0.9990
unsw->cic GBT      0.9136  0.9666       0.0631       0.9667
          MLP      0.9656  0.9565       0.1639       0.9594
          RF       0.9662  0.9636       0.1994       0.9638

## E4b TAN-IDS 5% budget F1 (shared)
 method           finetune  pooled  source-only  target-only
direction model                                            
cic->unsw GBT      0.9974  0.9988       0.0089       0.9996
          MLP      0.9982  0.9942       0.0535       0.9975
          RF       0.9813  0.9989       0.0015       0.9990
unsw->cic GBT      0.9422  0.9668       0.1786       0.9667
          MLP      0.9659  0.9562       0.2625       0.9607
          RF       0.9677  0.9636       0.2095       0.9638
E4b target labels per run (shared): {'cic->unsw': 82789, 'unsw->cic': 70404}

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
Runs with MIN_TTL or MAX_TTL among first 5 removed (raw): 24 of 36

## Single-feature AUC>=0.99: raw 13 zscore 231 of 270
cic-unsw PROTOCOL: [{'raw': 0.565, 'zscore': 1.0}]

## Verdicts by k, per-domain
 verdict  help  hurt  no diff
k                           
1           9    27       72
5           3    31       74
10          4    35       69
50          8    31       69
100        10    29       69
verdicts by pair (sorted by net), per-domain
 verdict    help  hurt  no diff  net
direction                          
ton->cic      9     5       31    4
unsw->ton     2     5       38   -3
unsw->bot     5    10       30   -5
ton->unsw     2     9       34   -7
bot->ton      0     8       37   -8
ton->bot      6    14       25   -8
cic->ton      1    11       33  -10
cic->unsw     0    11       34  -11
bot->cic      3    16       26  -13
unsw->cic     0    14       31  -14
cic->bot      5    24       16  -19
bot->unsw     1    26       18  -25
unsw->bot helps at k, per-domain: {1: 3, 100: 2} hurts at k: {1: 1, 5: 4, 10: 3, 50: 1, 100: 1}
bot->cic helps at k, per-domain: {1: 3} hurts at k: {1: 3, 5: 1, 10: 3, 50: 4, 100: 5}
Benjamini-Hochberg (q=0.05) rejections, per-domain: 129 help 19 hurt 110

## Verdicts by k, shared
 verdict  help  hurt  no diff
k                           
1          11    28       69
5           6    37       65
10          5    35       68
50          8    56       44
100        11    49       48
verdicts by pair (sorted by net), shared
 verdict    help  hurt  no diff  net
direction                          
unsw->bot     9     3       33    6
unsw->ton     3     3       39    0
bot->cic     14    16       15   -2
ton->unsw     1    13       31  -12
cic->bot      7    21       17  -14
ton->bot      6    23       16  -17
cic->unsw     0    18       27  -18
ton->cic      0    18       27  -18
unsw->cic     0    20       25  -20
bot->ton      1    22       22  -21
cic->ton      0    23       22  -23
bot->unsw     0    25       20  -25
unsw->bot helps at k, shared: {1: 2, 10: 2, 50: 2, 100: 3} hurts at k: {50: 2, 100: 1}
bot->cic helps at k, shared: {1: 7, 5: 5, 10: 2} hurts at k: {10: 3, 50: 6, 100: 7}
Benjamini-Hochberg (q=0.05) rejections, shared: 179 help 29 hurt 150

## E6 pooled mean delta over pairs, pair-bootstrap 95% CI
         scaling metric  mean_delta  ci_low  ci_high  pairs_positive  n_pairs                                                  mean_delta_by_k
     per-domain     f1     -0.0385 -0.0645  -0.0169               1       12   {1: -0.0521, 5: -0.051, 10: -0.043, 50: -0.0278, 100: -0.0183}
     per-domain   bacc     -0.0142 -0.0225  -0.0058               3       12  {1: -0.0151, 5: -0.0199, 10: -0.0166, 50: -0.0116, 100: -0.008}
         shared     f1     -0.0439 -0.0655  -0.0224               3       12  {1: -0.043, 5: -0.0688, 10: -0.0472, 50: -0.0345, 100: -0.0256}
         shared   bacc     -0.0181 -0.0334  -0.0020               3       12 {1: -0.0053, 5: -0.0345, 10: -0.0246, 50: -0.0159, 100: -0.0099}
no-TTL (shared)     f1     -0.0562 -0.0797  -0.0298               2       12 {1: -0.0459, 5: -0.0919, 10: -0.0685, 50: -0.0461, 100: -0.0287}
no-TTL (shared)   bacc     -0.0293 -0.0473  -0.0111               3       12 {1: -0.0047, 5: -0.0555, 10: -0.0447, 50: -0.0253, 100: -0.0161}

## E6 verdicts by metric
 verdict                 help  hurt  no diff
scaling         metric                     
no-TTL (shared) bacc      35   254      251
                f1        42   228      270
per-domain      bacc      49   147      344
                f1        34   153      353
shared          bacc      35   214      291
                f1        41   205      294
BoT-target cells, bacc
 verdict          help  hurt  no diff
scaling                             
no-TTL (shared)    17    37       81
per-domain         32    15       88
shared             13    36       86

## E6 within-dataset domain AUC control (two random halves), mean over seeds
 scaling     raw  zscore
dataset                
bot      0.5014     1.0
cic      0.4986     1.0
ton      0.5013     1.0
unsw     0.4983     1.0

## E1 (per-domain) paired source-vs-target-only, F1 (Wilcoxon over 10 seeds), all features vs -TTL
 direction features   k              mode  delta  seeds_pos     p
cic->unsw     -TTL   1          source+k -0.088          3 0.064
cic->unsw     -TTL   1 source+k-weighted -0.100          2 0.027
cic->unsw     -TTL   5          source+k  0.042          7 0.432
cic->unsw     -TTL   5 source+k-weighted  0.167          8 0.037
cic->unsw     -TTL  10          source+k  0.039          6 0.770
cic->unsw     -TTL  10 source+k-weighted  0.147          8 0.014
cic->unsw     -TTL  50          source+k -0.006          3 0.275
cic->unsw     -TTL  50 source+k-weighted  0.006          4 0.625
cic->unsw     -TTL 100          source+k  0.015          5 0.275
cic->unsw     -TTL 100 source+k-weighted  0.005          3 0.770
cic->unsw      all   1          source+k -0.047          2 0.160
cic->unsw      all   1 source+k-weighted -0.025          3 0.770
cic->unsw      all   5          source+k  0.003          6 1.000
cic->unsw      all   5 source+k-weighted  0.056          6 0.432
cic->unsw      all  10          source+k -0.036          2 0.084
cic->unsw      all  10 source+k-weighted  0.020          4 0.770
cic->unsw      all  50          source+k -0.041          0 0.002
cic->unsw      all  50 source+k-weighted -0.007          0 0.002
cic->unsw      all 100          source+k -0.004          1 0.014
cic->unsw      all 100 source+k-weighted -0.004          1 0.027
unsw->cic     -TTL   1          source+k  0.042          7 0.492
unsw->cic     -TTL   1 source+k-weighted -0.003          5 1.000
unsw->cic     -TTL   5          source+k  0.016          5 0.625
unsw->cic     -TTL   5 source+k-weighted  0.048          7 0.160
unsw->cic     -TTL  10          source+k  0.034          5 0.770
unsw->cic     -TTL  10 source+k-weighted  0.076          7 0.064
unsw->cic     -TTL  50          source+k  0.030          9 0.027
unsw->cic     -TTL  50 source+k-weighted -0.004          5 0.695
unsw->cic     -TTL 100          source+k  0.011          9 0.004
unsw->cic     -TTL 100 source+k-weighted  0.003          7 0.275
unsw->cic      all   1          source+k -0.034          2 0.131
unsw->cic      all   1 source+k-weighted -0.031          2 0.322
unsw->cic      all   5          source+k -0.020          4 0.846
unsw->cic      all   5 source+k-weighted -0.003          6 0.770
unsw->cic      all  10          source+k -0.025          2 0.275
unsw->cic      all  10 source+k-weighted -0.024          4 0.557
unsw->cic      all  50          source+k  0.030          8 0.049
unsw->cic      all  50 source+k-weighted -0.015          3 0.193
unsw->cic      all 100          source+k  0.006          5 0.846
unsw->cic      all 100 source+k-weighted  0.003          5 0.625
E1 (per-domain) mean F1 by direction/features/mode, k=1..10
 features         -TTL                                    all                              
mode         source+k source+k-weighted target-only source+k source+k-weighted target-only
direction k                                                                               
cic->unsw 1     0.074             0.062       0.162    0.107             0.130       0.154
          5     0.542             0.667       0.500    0.700             0.754       0.697
          10    0.635             0.743       0.596    0.775             0.832       0.811
unsw->cic 1     0.344             0.299       0.302    0.262             0.266       0.297
          5     0.426             0.459       0.411    0.390             0.407       0.410
          10    0.573             0.614       0.539    0.530             0.531       0.555

## E1 (shared) paired source-vs-target-only, F1 (Wilcoxon over 10 seeds), all features vs -TTL
 direction features   k              mode  delta  seeds_pos     p
cic->unsw     -TTL   1          source+k -0.129          1 0.010
cic->unsw     -TTL   1 source+k-weighted -0.141          0 0.002
cic->unsw     -TTL   5          source+k -0.316          1 0.004
cic->unsw     -TTL   5 source+k-weighted -0.263          0 0.002
cic->unsw     -TTL  10          source+k -0.144          3 0.275
cic->unsw     -TTL  10 source+k-weighted -0.133          4 0.193
cic->unsw     -TTL  50          source+k -0.015          5 0.432
cic->unsw     -TTL  50 source+k-weighted -0.015          6 0.770
cic->unsw     -TTL 100          source+k -0.001          6 0.922
cic->unsw     -TTL 100 source+k-weighted  0.002          4 1.000
cic->unsw      all   1          source+k -0.114          1 0.006
cic->unsw      all   1 source+k-weighted -0.115          1 0.006
cic->unsw      all   5          source+k -0.277          2 0.010
cic->unsw      all   5 source+k-weighted -0.385          0 0.002
cic->unsw      all  10          source+k -0.086          2 0.432
cic->unsw      all  10 source+k-weighted -0.151          2 0.375
cic->unsw      all  50          source+k -0.012          2 0.432
cic->unsw      all  50 source+k-weighted -0.024          2 0.322
cic->unsw      all 100          source+k -0.000          1 0.084
cic->unsw      all 100 source+k-weighted -0.003          1 0.084
unsw->cic     -TTL   1          source+k -0.028          4 0.492
unsw->cic     -TTL   1 source+k-weighted -0.036          2 0.193
unsw->cic     -TTL   5          source+k -0.024          3 0.557
unsw->cic     -TTL   5 source+k-weighted -0.042          4 0.322
unsw->cic     -TTL  10          source+k -0.062          1 0.014
unsw->cic     -TTL  10 source+k-weighted -0.073          1 0.064
unsw->cic     -TTL  50          source+k -0.057          2 0.014
unsw->cic     -TTL  50 source+k-weighted -0.111          0 0.002
unsw->cic     -TTL 100          source+k -0.049          0 0.002
unsw->cic     -TTL 100 source+k-weighted -0.069          0 0.002
unsw->cic      all   1          source+k -0.025          4 0.432
unsw->cic      all   1 source+k-weighted -0.043          3 0.232
unsw->cic      all   5          source+k -0.021          5 0.846
unsw->cic      all   5 source+k-weighted -0.042          3 0.375
unsw->cic      all  10          source+k -0.101          1 0.004
unsw->cic      all  10 source+k-weighted -0.124          0 0.002
unsw->cic      all  50          source+k -0.054          1 0.027
unsw->cic      all  50 source+k-weighted -0.071          0 0.002
unsw->cic      all 100          source+k -0.027          0 0.002
unsw->cic      all 100 source+k-weighted -0.040          1 0.004
E1 (shared) mean F1 by direction/features/mode, k=1..10
 features         -TTL                                    all                              
mode         source+k source+k-weighted target-only source+k source+k-weighted target-only
direction k                                                                               
cic->unsw 1     0.034             0.022       0.163    0.041             0.039       0.155
          5     0.183             0.236       0.500    0.421             0.312       0.697
          10    0.450             0.461       0.594    0.726             0.661       0.811
unsw->cic 1     0.274             0.266       0.302    0.270             0.252       0.295
          5     0.381             0.364       0.406    0.381             0.360       0.402
          10    0.477             0.465       0.538    0.454             0.430       0.555

## No-TTL (shared) F1 verdicts by pair
 verdict    help  hurt  no diff  net
direction                          
unsw->bot    15     0       30   15
ton->unsw     0     4       41   -4
bot->unsw     5    15       25  -10
bot->cic      6    18       21  -12
cic->unsw     0    13       32  -13
bot->ton      4    21       20  -17
cic->bot      6    24       15  -18
unsw->ton     0    19       26  -19
ton->bot      6    28       11  -22
unsw->cic     0    23       22  -23
ton->cic      0    31       14  -31
cic->ton      0    32       13  -32
