import pandas as pd
import time
from pprint import pprint

# list of public transportation coordinate points
transp = [[-23.4584161,-46.5692977],[-23.4633841,-46.5818462],[-23.4716607,-46.5976793],[-23.4800303,-46.603175],[-23.4869898,-46.608824],[-23.4924608,-46.6170636],[-23.5025828,-46.6247481],[-23.5091844,-46.6249466],[-23.5162457,-46.6251571],[-23.5254647,-46.6293668],[-23.5307851,-46.6322972],[-23.5365751,-46.6339495],[-23.5441352,-46.6340876],[-23.5506309,-46.632898],[-23.5552951,-46.6359074],[-23.5618371,-46.6386594],[-23.568823,-46.6399133],[-23.5757692,-46.6407065],[-23.5813846,-46.6384227],[-23.5894897,-46.6347548],[-23.5988865,-46.6366732],[-23.6106163,-46.6379057],[-23.6185506,-46.6392293],[-23.6256381,-46.6408307],[-23.6353764,-46.6412617],[-23.6464751,-46.6409333],[-23.4883317,-46.5473932],[-23.4984701,-46.5514098],[-23.509123,-46.5587845],[-23.5170597,-46.5506293],[-23.5231787,-46.5452146],[-23.5327303,-46.5428287],[-23.5397632,-46.5412844],[-23.5471776,-46.5415064],[-23.5539688,-46.5450449],[-23.5623215,-46.550642],[-23.5629148,-46.5600035],[-23.5735155,-46.5669907],[-23.577613,-46.5763712],[-23.5843479,-46.5819192],[-23.5929991,-46.5896876],[-23.6015736,-46.6031108],[-23.6021751,-46.6124609],[-23.5958995,-46.6207711],[-23.5924442,-46.6305846],[-23.5814356,-46.6385093],[-23.5757501,-46.640844],[-23.5682612,-46.6482255],[-23.5631678,-46.6544053],[-23.556913,-46.6616024],[-23.5540954,-46.6708117],[-23.5508725,-46.6777566],[-23.5465746,-46.6906821],[-23.5406087,-46.7022081],[-23.5345789,-46.7132097],[-23.5285663,-46.7253201],[-23.5232419,-46.7375724],[-23.519516,-46.753148],[-23.5092576,-46.7637214],[-23.5423403,-46.4709288],[-23.5405796,-46.484313],[-23.5310138,-46.5017151],[-23.5292923,-46.5165586],[-23.531872,-46.5308869],[-23.5335222,-46.5425224],[-23.5378846,-46.5645111],[-23.5404222,-46.5763316],[-23.542896,-46.5896702],[-23.5463581,-46.6070348],[-23.5478654,-46.6158727],[-23.5497071,-46.6259283],[-23.5506199,-46.6328933],[-23.5479515,-46.6389611],[-23.5442483,-46.6428236],[-23.5390058,-46.6493869],[-23.5337336,-46.655851],[-23.5260167,-46.667465],[-23.5459992,-46.60575],[-23.5393108,-46.6088131],[-23.535187,-46.615996],[-23.5326959,-46.625432],[-23.5364263,-46.6343906],[-23.5443935,-46.6427672],[-23.5491834,-46.6526323],[-23.5550574,-46.6621542],[-23.5603091,-46.67165990000001],[-23.56619,-46.6841671],[-23.5675299,-46.6939786],[-23.567284,-46.7017918],[-23.5718961,-46.7081514],[-23.5864834,-46.7240515],[-23.5935355,-46.7350405],[-23.6022365,-46.743967],[-23.6092191,-46.7560637],[-23.624649,-46.7646092],[-23.6336587,-46.7737878],[-23.6423424,-46.7798281],[-23.6539098,-46.7771995],[-23.6596587,-46.7665351],[-23.6661825,-46.7542774],[-23.669123,-46.7357158],[-23.582135,-46.5970993],[-23.5835706,-46.6078174],[-23.5873938,-46.6195386],[-23.5927699,-46.6307322],[-23.5984258,-46.6369776],[-23.598111,-46.6455258],[-23.5975451,-46.6521937],[-23.6034999,-46.6621575],[-23.609718,-46.6683849],[-23.6186625,-46.6820642],[-23.6267659,-46.6879972],[-23.6334707,-46.6927274],[-23.6413951,-46.699296],[-23.6500622,-46.7041496],[-23.6541603,-46.7080039],[-23.6557106,-46.7206934],[-23.6439541,-46.734075],[-23.640217,-46.7456353],[-23.6491716,-46.7588867],[-23.6594032,-46.7681337],[-23.6762579,-46.7746971],[-23.6897947,-46.7739889],[-23.4343527,-46.7196125],[-23.4396339,-46.7083848],[-23.4496166,-46.7007362],[-23.4627346,-46.7013574],[-23.4704798,-46.6980315],[-23.4761039,-46.6989112],[-23.4862714,-46.6933402],[-23.4933881,-46.6917336],[-23.5018645,-46.693579],[-23.5140839,-46.6919535],[-23.5211239,-46.6880778],[-23.5273251,-46.6835206],[-23.5321795,-46.6759193],[-23.5382264,-46.6695598],[-23.5455172,-46.6603571],[-23.5500858,-46.6533458],[-23.5561884,-46.6494942],[-23.5615211,-46.64509],[-23.5627825,-46.6392213],[-23.5720961,-46.6287923],[-23.5786715,-46.6240179],[-23.587135,-46.6194475],[-23.5928398,-46.6101509],[-23.6017965,-46.6031128],[-23.6203767,-46.5920785],[-23.6329098,-46.5831196],[-23.6510652,-46.5763336],[-23.1950499,-46.8721211],[-23.2089642,-46.8292866],[-23.2064731,-46.7857343],[-23.236306,-46.7670446],[-23.2616044,-46.754087],[-23.2816169,-46.7425776],[-23.3099637,-46.7236164],[-23.329469,-46.726141],[-23.3561661,-46.7427056],[-23.3661555,-46.7515648],[-23.3747223,-46.7557244],[-23.4047292,-46.7538831],[-23.4162068,-46.7448414],[-23.4380934,-46.7471588],[-23.455727,-46.7383611],[-23.4725735,-46.7395171],[-23.4699093,-46.7443541],[-23.4874729,-46.72743],[-23.4964012,-46.7179281],[-23.5040235,-46.7150216],[-23.5072396,-46.714511],[-23.5189505,-46.7006983],[-23.5176682,-46.7036865],[-23.5454268,-46.6165502],[-23.5580668,-46.6083196],[-23.5669091,-46.6040643],[-23.582205,-46.5967768],[-23.5925586,-46.5895629],[-23.6100129,-46.5701034],[-23.6153313,-46.5547425],[-23.6254267,-46.544534],[-23.6391284,-46.5362191],[-23.6521555,-46.5281403],[-23.6586096,-46.4912384],[-23.6673898,-46.4627185],[-23.6899384,-46.4499243],[-23.7013726,-46.4351481],[-23.7129448,-46.4154312],[-23.7428057,-46.3924111],[-23.7632632,-46.3765526],[-23.7680206,-46.3420084],[-23.7779961,-46.3032183],[-23.5344299,-46.6383743],[-23.5279786,-46.6485591],[-23.5254872,-46.6676028],[-23.5238001,-46.6799758],[-23.5214331,-46.6884818],[-23.5188109,-46.721439],[-23.5237566,-46.737602],[-23.5311663,-46.76175],[-23.5276152,-46.7760006],[-23.5257019,-46.7956209],[-23.5227054,-46.8072121],[-23.5234639,-46.8155042],[-23.5184985,-46.8353713],[-23.5165974,-46.847983],[-23.517325400000004,-46.8578213],[-23.5126721,-46.8756527],[-23.5140691,-46.8893373],[-23.5235329,-46.8935403],[-23.5279767,-46.9030058],[-23.5291977,-46.9160193],[-23.535218900000004,-46.9286263],[-23.5449984,-46.9472971],[-23.5414452,-46.9602764],[-23.5313875,-46.971885],[-23.5304924,-46.9837564],[-23.5276938,-46.7760796],[-23.5312485,-46.7616789],[-23.537437,-46.7426473],[-23.5460434,-46.7328626],[-23.5576636,-46.711818],[-23.5669276,-46.7028701],[-23.5737374,-46.6986805],[-23.5853404,-46.6911489],[-23.5935061,-46.6927153],[-23.6047141,-46.6967815],[-23.6215931,-46.7016202],[-23.627520400000005,-46.7119306],[-23.6389107,-46.722731],[-23.656229,-46.7191699],[-23.6634027,-46.7109221],[-23.6774444,-46.7022184],[-23.6881245,-46.6947055],[-23.7062109,-46.688405],[-23.7224874,-46.6917926],[-23.7364785,-46.6970819],[-23.7543619,-46.7093128],[-23.7709123,-46.7119788],[-23.7829493,-46.7095648],[-23.7958001,-46.7048979],[-23.8229946,-46.7014861],[-23.5252236,-46.6675935],[-23.5277782,-46.648649],[-23.5349728,-46.6356439],[-23.538498,-46.6230929],[-23.545307,-46.6162951],[-23.5401271,-46.5763905],[-23.533312,-46.542525],[-23.5420108,-46.4709931],[-23.5418115,-46.4481193],[-23.5390895,-46.4316774],[-23.542264,-46.4158094],[-23.5476318,-46.39911],[-23.5543689,-46.3836148],[-23.540855,-46.3684469],[-23.5253659,-46.3435419],[-23.5342389,-46.3078249],[-23.5220449,-46.1988287],[-23.5149471,-46.182642],[-23.5452589,-46.6162079],[-23.5425985,-46.5897506],[-23.5399846,-46.5763932],[-23.5287636,-46.5533611],[-23.516686,-46.5506896],[-23.5043808,-46.5385661],[-23.4980292,-46.5197677],[-23.4854769,-46.5012646],[-23.485103,-46.4822799],[-23.4897856,-46.4630418],[-23.4905592,-46.4437178],[-23.4927166,-46.421104],[-23.4939835,-46.4023339],[-23.484777,-46.3852805],[-23.4795039,-46.3689485],[-23.4808914,-46.3518656],[-23.4894719,-46.3360727],[-23.507448,-46.3377464],[-23.5252802,-46.3330941],[-23.5341246,-46.3077995],[-23.534491,-46.2851912],[-23.541873,-46.2636799],[-23.5407075,-46.2400201],[-23.5342254,-46.2188066],[-23.5219662,-46.1988589],[-23.5148807,-46.1826744],[-23.4242206,-46.407339],[-23.4142894,-46.4282226],[-23.41441,-46.4541141],[-23.4194114,-46.4823476],[-23.4330632,-46.4937705],[-23.4477078,-46.4936766],[-23.4622074,-46.4895675],[-23.4979455,-46.5198148],[-23.5043353,-46.538609],[-23.5166933,-46.5507902],[-23.5287317,-46.553565],[-23.5400387,-46.5419316],[-23.5466557,-46.5276569],[-23.5550131,-46.5173197],[-23.5671217,-46.5063548],[-23.5822283,-46.4916992],[-23.5943517,-46.4951324],[-23.6143949,-46.5013153],[-23.626979,-46.5036407],[-23.6403662,-46.50777],[-23.6517886,-46.528073],[-23.5942778,-46.6911489],[-23.6056505,-46.6930158],[-23.6139403,-46.6960412],[-23.6234055,-46.6997212],[-23.627771,-46.7076311],[-23.6370446,-46.7153477],[-23.6471998,-46.7168202],[-23.6559686,-46.7205458],[-23.6635551,-46.7264145],[-23.6693183,-46.7353704],[-23.6751255,-46.7486072],[-23.678255,-46.7626888],[-23.6857715,-46.7703384],[-23.6928502,-46.7784092],[-23.700459,-46.7814132],[-23.7130552,-46.7816895],[-23.7256993,-46.786083],[-23.5822529,-46.5968022],[-23.5847455,-46.583139],[-23.582141,-46.5616183],[-23.5888702,-46.5446573],[-23.5953201,-46.5377534],[-23.6008995,-46.5271479],[-23.6029346,-46.5158343],[-23.6063854,-46.5077341],[-23.6146137,-46.5004974],[-23.6118808,-46.4876175],[-23.6122274,-46.4773151],[-23.5988644,-46.4687347],[-23.5967408,-46.4564449],[-23.5946859,-46.4437473],[-23.5942312,-46.424025],[-23.5826265,-46.4151013],[-23.5836344,-46.4090234],[-23.5993646,-46.401937],[-23.5606324,-46.6717511],[-23.5648402,-46.6670332],[-23.5696773,-46.661548],[-23.574931,-46.656071],[-23.5756476,-46.6410613],[-23.5714134,-46.629593],[-23.5675069,-46.621702],[-23.567888,-46.6124296],[-23.5667432,-46.6044143],[-23.5632766,-46.5972609],[-23.5588732,-46.5862968],[-23.5550955,-46.577139],[-23.5591425,-46.5681812],[-23.5627529,-46.5603429],[-23.5706693,-46.5505073],[-23.5731032,-46.5407923],[-23.5730932,-46.5330112],[-23.5721935,-46.5247554],[-23.5649385,-46.5132273],[-23.5650174,-46.5072057],[-23.6215145,-46.7017678],[-23.6139821,-46.6956094],[-23.6155733,-46.6885968],[-23.6185506,-46.6834201],[-23.6219519,-46.6789609],[-23.6294371,-46.6736783],[-23.6269601,-46.6618766],[-23.6345531,-46.6683957],[-23.6382144,-46.6618162],[-23.6437465,-46.65729],[-23.6504431,-46.6516064],[-23.6588375,-46.6445308],[-23.6663481,-46.6381608],[-23.6733037,-46.6378705],[-23.6814532,-46.6379231],[-23.6852016,-46.6267276],[-23.4736536,-46.6704315],[-23.4848816,-46.6648311],[-23.4950804,-46.6614783],[-23.5033256,-46.6549551],[-23.5110438,-46.653201],[-23.5225097,-46.6509264],[-23.5279998,-46.6486797],[-23.5342058,-46.6440761],[-23.5393698,-46.6403103],[-23.543523,-46.6356566],[-23.5451533,-46.6291738],[-23.5443935,-46.6233184],[-23.543181,-46.6168807],[-23.5390256,-46.6073191],[-23.537137,-46.5936935],[-23.5346287,-46.5757764],[-23.5327598,-46.5659059],[-23.5288399,-46.5537179],[-23.5231989,-46.5452253],[-23.5935858,-46.6917204],[-23.5906018,-46.6816187],[-23.585827,-46.6710377],[-23.579362,-46.6619128],[-23.5738702,-46.6555238],[-23.5681691,-46.6494567],[-23.5618334,-46.6445911],[-23.5554705,-46.6418445],[-23.5497268,-46.6385078],[-23.5442779,-46.6349244],[-23.5410566,-46.6287017],[-23.5390157,-46.6225272],[-23.535182,-46.6159907],[-23.5328532,-46.601311],[-23.5225491,-46.5929854],[-23.5150824,-46.5871596],[-23.5076792,-46.5812695],[-23.498844,-46.5729976],[-23.4891669,-46.5653693],[-23.4854523,-46.5571189],[-23.4875138,-46.5476024],[-23.4784558,-46.5361762],[-23.46923,-46.5306723],[-23.4540636,-46.5340572],[-23.5141232,-46.6915834],[-23.5195437,-46.7003703],[-23.5283333,-46.702559],[-23.5403829,-46.7032081],[-23.55311,-46.6958159],[-23.5612852,-46.6932517],[-23.5674684,-46.6930425],[-23.5713232,-46.6906392],[-23.5813335,-46.6845345],[-23.5905761,-46.681391],[-23.5975125,-46.673886],[-23.6034999,-46.6621575],[-23.6096,-46.6543865],[-23.6185458,-46.6482389],[-23.6259673,-46.6410076],[-23.6288669,-46.6273605],[-23.6341163,-46.6160682],[-23.6411039,-46.6072332],[-23.6447306,-46.5969872],[-23.6477773,-46.5871382],[-23.6511827,-46.5758997],[-23.6535149,-46.5629573],[-23.6554018,-46.548806],[-23.656188,-46.535454],[-23.6522312,-46.5281128],[-23.5652457,-46.5071681],[-23.5598614,-46.498813],[-23.5536729,-46.4912921],[-23.5504765,-46.4814645],[-23.5424753,-46.4726487],[-23.5304049,-46.4738557],[-23.5174493,-46.4758674],[-23.5159727,-46.4669483],[-23.5153382,-46.4553988],[-23.5134296,-46.4439457],[-23.509573,-46.4293384],[-23.5096222,-46.4168286],[-23.5118457,-46.4020872],[-23.510884,-46.3943893],[-23.5073791,-46.3876301],[-23.5004281,-46.3792777],[-23.4923252,-46.3782397],[-23.4845985,-46.3849564],[-23.4764309,-46.3891031],[-23.4671804,-46.3903584],[-23.4634087,-46.395004],[-23.4607317,-46.4026161],[-23.453382,-46.4064248],[-23.4403328,-46.4075504],[-23.4327261,-46.4053671],[-23.4243091,-46.4071137],[-23.5405327,-46.7030342],[-23.550489,-46.7070308],[-23.5582805,-46.7114778],[-23.5718534,-46.7083075],[-23.5776363,-46.7247999],[-23.5841752,-46.7365265],[-23.5864711,-46.7574424],[-23.5830641,-46.7738038],[-23.5888407,-46.7944139],[-23.591166,-46.8189079],[-23.5971439,-46.8412828],[-23.596844,-46.8603748],[-23.5968661,-46.8806362],[-23.5989578,-46.8926203],[-23.6012732,-46.907437],[-23.6043798,-46.9222185],[-23.5280385,-46.7756827],[-23.5163726,-46.7754959],[-23.5092431,-46.7637292],[-23.5006906,-46.7546578],[-23.4909565,-46.7507142],[-23.4840366,-46.7427964],[-23.4874056,-46.7273243],[-23.4974492,-46.7070843],[-23.5022827,-46.6939545],[-23.5041767,-46.6815309],[-23.5059525,-46.668983],[-23.503611,-46.6546762],[-23.4997246,-46.6452616],[-23.5002362,-46.6345275],[-23.5016579,-46.6250968],[-23.5018793,-46.6120827],[-23.5068823,-46.6010106],[-23.5076202,-46.5813339],[-23.516563,-46.5685665],[-23.5166245,-46.5506059],[-23.5146791,-46.5304551],[-23.5978481,-46.720047],[-23.6161644,-46.7209536],[-23.6533692,-46.5631163],[-23.6629949,-46.5560299],[-23.668768,-46.5528595],[-23.6792425,-46.5540612],[-23.6858156,-46.5507245],[-23.6972564,-46.5510732],[-23.7030624,-46.5525752],[-23.7099536,-46.5523446],[-23.720105500000003,-46.5506923],[-23.7257631,-46.56137820000001],[-23.7285771,-46.56744],[-23.7280369,-46.5748],[-23.5227557,-46.5318847],[-23.5149643,-46.5200722],[-23.5119145,-46.5119935],[-23.5133706,-46.5011895],[-23.5149938,-46.4893556],[-23.5166564,-46.4768565],[-23.5406928,-46.5416425],[-23.6538066,-46.707226],[-23.6585655,-46.6984847],[-23.6632799,-46.6917014],[-23.6656676,-46.6775127],[-23.6744525,-46.6625297],[-23.6816006,-46.6529488],[-23.6875694,-46.6399079],[-23.6859532,-46.6257351],[-23.6858402,-46.6135687],[-23.6890775,-46.5956891],[-23.6975364,-46.5784478],[-23.6996977,-46.5637494],[-23.6976248,-46.5510517],[-23.7032245,-46.5406823],[-23.7096294,-46.5294546],[-23.7042952,-46.5185152],[-23.6981504,-46.5060416],[-23.6874171,-46.5071788],[-23.676398,-46.5110439],[-23.6647097,-46.5121865],[-23.6584328,-46.511862],[-23.6523963,-46.5277702],[-23.5177091,-46.4758641],[-23.5390034,-46.6484535],[-23.5288448,-46.5543669],[-23.5493702,-46.6396773],[-23.6314865,-46.7721945],[-23.6544699,-46.7619485],[-23.4961481,-46.6625941],[-23.5834033,-46.4079157],[-23.5420354,-46.4492673],[-23.5418743,-46.4163418],[-23.5428886,-46.4160964],[-23.4941974,-46.4017412],[-23.5396772,-46.4315781],[-23.6844548,-46.6263494],[-23.7203904,-46.5511135],[-23.7366455,-46.6967681],[-23.6688172,-46.7354804],[-23.6462834,-46.6400287],[-23.6905439,-46.774115],[-23.4320247,-46.7870754],[-23.6436839,-46.7340159],[-23.5201193,-46.700027],[-23.5471892,-46.6290879],[-23.5402649,-46.4834949],[-23.5425124,-46.5901852],[-23.543046,-46.5887287],[-23.5472384,-46.6157949],[-23.5720288,-46.7089614],[-23.6494701,-46.7587647],[-23.659644,-46.7675409],[-23.5371173,-46.5639156],[-23.5385755,-46.5636232],[-23.542537,-46.4710039],[-23.5286247,-46.5164244],[-23.5244723,-46.6672879],[-23.5261962,-46.6674784],[-23.5300252,-46.5010124],[-23.5330082,-46.5439063],[-23.5341566,-46.5427288],[-23.6555165,-46.7225093],[-23.5858369,-46.7238342],[-23.5938256,-46.5901919],[-23.5396821,-46.5768975],[-23.5412067,-46.5766749],[-23.5471302,-46.6903549],[-23.5312745,-46.5295109],[-23.5323541,-46.5311202],[-23.8282944,-46.7271307],[-23.547022,-46.6301018],[-23.5188822,-46.5469694],[-23.5664063,-46.7018777],[-23.6917155,-46.5850487],[-23.4863035,-46.7263502],[-23.5343214,-46.6446716],[-23.6031263,-46.6026333],[-23.6519565,-46.5267],[-23.6529221,-46.5291086],[-23.6542242,-46.7113298],[-23.6982781,-46.5522212],[-23.6135937,-46.4759659],[-23.4916367,-46.4347512],[-23.6141689,-46.5009239],[-23.6245174,-46.4807215],[-23.7671074,-46.7164367],[-23.5583987,-46.5228027],[-23.4749427,-46.6700131],[-23.5845194,-46.5835762],[-23.6494161,-46.6405141],[-23.6528472,-46.637148],[-23.6563162,-46.6363835],[-23.6614865,-46.6373974],[-23.6656273,-46.638025],[-23.6691377,-46.6346844],[-23.6706535,-46.6326298],[-23.6738494,-46.6309252],[-23.677383,-46.6275832],[-23.6863806,-46.6245121],[-23.6865034,-46.6215804],[-23.6860956,-46.6184986],[-23.6858967,-46.6137443],[-23.6828435,-46.6050446],[-23.6796945,-46.5991947],[-23.6818548,-46.5952787],[-23.6864506,-46.5927212],[-23.6894337,-46.5905432],[-23.6917818,-46.5814787],[-23.690367,-46.5770182],[-23.689468,-46.5725631],[-23.6897259,-46.5689085],[-23.6895405,-46.5629996],[-23.6915386,-46.5571578],[-23.6938977,-46.5534952],[-23.7034701,-46.5524009],[-23.7078207,-46.5527013],[-23.7120668,-46.5521622],[-23.7151352,-46.5517598],[-23.717586,-46.5512891],[-23.6209652,-46.4784269],[-23.6237139,-46.4810514],[-23.6247165,-46.4872487],[-23.6258911,-46.4912626],[-23.626041,-46.4958693],[-23.6259427,-46.5011667],[-23.6272329,-46.504793],[-23.6283387,-46.5098946],[-23.6312739,-46.5108146],[-23.6338135,-46.5121476],[-23.6363813,-46.5160221],[-23.6387083,-46.5191656],[-23.6412133,-46.5214764],[-23.6444726,-46.5233485],[-23.6473792,-46.5248573],[-23.6556762,-46.5316728],[-23.660693,-46.5298489],[-23.6675508,-46.5323044],[-23.6705613,-46.5354252],[-23.6763267,-46.5365638],[-23.6808391,-46.5408795],[-23.6829688,-46.544935],[-23.6875129,-46.5476105],[-23.6915804,-46.5483776],[-23.6950091,-46.5503678],[-23.601082,-46.6913855],[-23.6074956,-46.6937097],[-23.6175063,-46.6973427],[-23.6130672,-46.6957193],[-23.6207618,-46.6984378],[-23.625678,-46.6918127],[-23.6261123,-46.6877827],[-23.6291054,-46.6849174],[-23.6336974,-46.6799627],[-23.6366479,-46.6775621],[-23.6411728,-46.6756021],[-23.6431059,-46.6735107],[-23.6488614,-46.670286],[-23.6524571,-46.6691527],[-23.6548519,-46.6670157],[-23.6570355,-46.6650355],[-23.6606936,-46.6631278],[-23.6640955,-46.6604751],[-23.6660719,-46.6566161],[-23.6675053,-46.6533653],[-23.6693601,-46.6490918],[-23.6722797,-46.6450759],[-23.6755904,-46.642324],[-23.6789551,-46.6405496],[-23.6817456,-46.6374082],[-23.6841269,-46.6333151],[-23.6214653,-46.7036801],[-23.6069199,-46.7253994],[-23.5505935,-46.6269416],[-23.5559167,-46.6229719],[-23.5590343,-46.6146624],[-23.5642072,-46.6112935],[-23.5694119,-46.607061],[-23.5744801,-46.6032059],[-23.5824524,-46.5997512],[-23.5913689,-46.5978879],[-23.5981434,-46.5972326],[-23.5857746,-46.5885691],[-23.5234091,-46.7005189],[-23.5249591,-46.6989954],[-23.5249975,-46.6952518],[-23.5250049,-46.6900752],[-23.5213225,-46.6987897],[-23.5223702,-46.696255],[-23.5227068,-46.6921777],[-23.5229832,-46.6882429],[-23.5251712,-46.6834117],[-23.5251951,-46.6823215],[-23.5257386,-46.6791887],[-23.5263701,-46.6738645],[-23.5278605,-46.6711181],[-23.5299238,-46.6673523],[-23.5319754,-46.6611429],[-23.5327082,-46.6574522],[-23.5345034,-46.6542389],[-23.5364092,-46.6508593],[-23.5385672,-46.6470435],[-23.5403868,-46.6437859],[-23.5445539,-46.6439039],[-23.5469735,-46.6427828],[-23.5475587,-46.6407229],[-23.5454722,-46.6383735],[-23.5426404,-46.6397036],[-23.5166098,-46.6985877],[-23.5138621,-46.7025524],[-23.5112119,-46.7054492],[-23.5062668,-46.7059994],[-23.5009987,-46.7065341],[-23.49825,-46.7068566],[-23.4950019,-46.7085368],[-23.4907491,-46.7101362],[-23.4882073,-46.7134921],[-23.4856551,-46.7156811],[-23.4838334,-46.716663],[-23.6586661,-46.5111619],[-23.5190624,-46.7007492],[-23.5455553,-46.9351977]]

deptos = [[-23.5569803, -46.6343707],[-23.539323, -46.6397243],[-23.6468944, -46.70744670000001],[-23.5369322, -46.6653372],[-23.5617968, -46.6912197],[-23.5295435, -46.6951429],[-23.5297112, -46.6123533],[-23.6017887, -46.6377481],[-23.6329013, -46.77042369999999],[-23.5506416, -46.6500727],[-23.5660725, -46.6692885],[-23.6054835, -46.4707403],[-23.639392, -46.6433401],[-23.5032146, -46.6127013],[-23.6647883, -46.7826795],[-23.5004813, -46.6491267],[-23.6043439, -46.692907],[-23.6152298, -46.67501009999999],[-23.5499136, -46.5677709],[-23.6629003, -46.7561995],[-23.5816982, -46.6745348],[-23.5288165, -46.5540478],[-23.5046049, -46.39673579999999],[-23.5657615, -46.638262],[-23.5909007, -46.6087102],[-23.5882146, -46.72672619999999],[-23.4586446, -46.5853353],[-23.7297691, -46.709445],[-23.5483289, -46.5937954],[-23.5366674, -46.6489398],[-23.4963086, -46.4412205],[-23.5790007, -46.6511819],[-23.6851295, -46.6372457],[-23.567624, -46.6235614],[-23.5240747, -46.4754671],[-23.6082362, -46.5008084],[-23.5793692, -46.5174278],[-23.4947594, -46.6977433],[-23.4832656, -46.5899297],[-23.5366448, -46.52656229999999],[-23.5987209, -46.5333003],[-23.5718195, -46.7225826],[-23.5099048, -46.4986202],[-23.4457366, -46.71685979999999],[-23.5587714, -46.7467711],[-23.4040925, -46.7380839],[-23.497318, -46.7457456],[-23.5546571, -46.49240460000001],[-23.5092849, -46.4463252],[-23.6929887, -46.7599783],[-23.606231, -46.593887],[-23.5426786, -46.4187947],[-23.6619864, -46.6870504],[-23.478257, -46.6207276],[-23.4695114, -46.6483016],[-23.7706354, -46.6971263],[-23.5342696, -46.4518314],[-23.5898428, -46.55329099999999],[-23.4898406, -46.4816704],[-23.5664039, -46.4669049],[-23.5228752, -46.7404531],[-23.6084649, -46.7360457],[-23.5009259, -46.5698395],[-23.523067, -46.64425139999999],[-23.4943279, -46.6778839],[-23.6566576, -46.66928919999999],[-23.5177596, -46.5847139],[-23.7121609, -46.6957234],[-23.6010108, -46.3985497],[-23.5938526, -46.5672439],[-23.4829978, -46.7279263],[-23.5973003, -46.7960428],[-23.6235926, -46.4702164],[-23.537349, -46.3976269],[-23.5363838, -46.5633524],[-23.8165554, -46.5834568],[-23.5519944, -46.4370144],[-23.5437622, -46.4814419],[-23.6731727, -46.659496],[-23.4702496, -46.6813993],[-23.8248915, -46.7343614],[-23.700726, -46.5768601],[-23.4875889, -46.4101492],[-23.6229114, -46.6019075],[-23.6565234, -46.6138129],[-23.5737271, -46.5576479],[-23.5689051, -46.5845589],[-23.5624913, -46.5452257],[-23.5491687, -46.53722570000001],[-23.4691612, -46.6897573],[-23.5202068, -46.41149069999999],[-23.5352219, -46.5846386],[-23.5704719, -46.5916469]]

final=[]

for dp in deptos:
    q=0
    inner = []
    for tp in transp:
        # ~2km in lat / long degrees near the equator is roughly 0.016
        # So we're considering a ~5km² square area around the police department
        if dp[0]-0.016 <= tp[0] <= dp[0]+0.016 and dp[1]-0.016 <= tp[1] <= dp[1]+0.016:
            q+=1
    inner.append(dp)
    inner.append(q)
    final.append(inner)

df=pd.DataFrame(final)
df.set_axis(['coordenada_dp', 'mobility_points'], axis=1, inplace=True)

# Save to file
t = time.localtime()
current_time = time.strftime("%b%d%Y%H:%M:%S", t)
df.to_csv(f'mobility_points_dps_{current_time}.csv',
          encoding='utf-8', index=False, header=True)