import Paillier

enc_data = 23003460961719600751144549386379034444445668997868483407421001599130041646295088971240620570659513528952261770024038938180253100923395322437572480579776777916472127316038500832549630706919819443800974585676098896806354462835505347601812943505549504584557768986685981371725611837518084630249180283989185994237

# const publicKey = [BigInt('9292770072280002632872384766929534187704042406374927299421759497484867499398448709157541684874762332977442863512477087398283677218674298619842062068118713'), BigInt('15358756879889351578838625081596159635274139051861385797559489777439838291132907758243816265063412349701422197035171747363819013261112999252404469915446046185826640108460741874088520082898327915390410786727896843993564847109934874886947930388392882621797849835302209575609304274087327679322157387232981713937')];
# const privateKey = [BigInt('4646385036140001316436192383464767093852021203187463649710879748742433749699127697383300203735056451044517707604817329375971485031963258310218181207526330'), BigInt('9271238385347014366247444470431759667446553307784074467263031788936248959877164780962817948330019336977554741633769585314194085215345022139428862935862515')];

pubkey = [9292770072280002632872384766929534187704042406374927299421759497484867499398448709157541684874762332977442863512477087398283677218674298619842062068118713, 15358756879889351578838625081596159635274139051861385797559489777439838291132907758243816265063412349701422197035171747363819013261112999252404469915446046185826630108460741874088520082898327915390410786727896843993564847109934874886947930388392882621797849835302209575609304274087327679322157387232981713937]
privkey = [4646385036140001316436192383464767093852021203187463649710879748742433749699127697383300203735056451044517707604817329375971485031963258310218181207526330, 9271238385347014366247444470431759667446553307784074467263031788936248959877164780962817948330019336977554741633769585314194085215345022139428862935862515]

print(Paillier.decrypt(privkey, pubkey, enc_data))