import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


numberUsersTested = [8, 16, 24, 32]

# Algorand data
users_eight_algo = [26.96867823600769, 29.96632170677185, 13.38296103477478, 14.163839101791382, 14.60978102684021, 14.284796237945557, 14.79357385635376, 14.242328882217407]
users_sixteen_algo = [31.235289096832275, 27.960975885391235, 36.717228174209595, 29.15287208557129, 51.15104627609253, 13.670492172241211, 15.32234501838684, 13.911133050918579, 15.070883750915527, 14.542326927185059, 17.835013151168823, 14.683258056640625, 14.507145881652832, 13.561905145645142, 14.358512878417969, 15.256983041763306]
users_twentyfour_algo = [29.187942028045654, 29.293426036834717, 29.23687982559204, 29.31158971786499, 28.901238918304443, 28.835137128829956, 14.799743890762329, 14.242055177688599, 15.295573949813843, 14.874115943908691, 13.871343851089478, 15.307765007019043, 13.626523971557617, 15.558722019195557, 14.278127193450928, 14.642388105392456, 14.767372131347656, 14.702378988265991, 13.639194965362549, 14.710679054260254, 14.849815845489502, 14.181243181228638, 15.240783929824829, 14.73969316482544]
users_thirtytwo_algo = [20.759005069732666, 22.827200174331665,21.441534996032715, 21.658177137374878, 21.620529890060425, 21.44936203956604, 22.538442134857178, 21.547117948532104, 7.208085060119629, 7.124981164932251, 8.457979917526245,6.171166896820068, 7.398247003555298, 7.806334972381592, 10.525480031967163, 8.489662885665894, 11.678270816802979, 9.773561000823975, 9.77493405342102, 7.547993183135986,7.652030944824219, 8.594905853271484, 9.930887222290039, 6.547883033752441, 7.571983098983765, 6.980309009552002, 7.5201191902160645, 6.98012900352478, 7.573504209518433, 10.736824989318848, 7.647424936294556, 7.6702001094818115]


deployAlgoMean = [np.mean(users_eight_algo[0:2]),np.mean(users_sixteen_algo[0:4]),np.mean(users_twentyfour_algo[0:6]),np.mean(users_thirtytwo_algo[0:8])] #mean values obtained during the four test (8,16,24,32) for Algorand
attachAlgoMean = [np.mean(users_eight_algo[2:8]),np.mean(users_sixteen_algo[4:16]),np.mean(users_twentyfour_algo[6:24]),np.mean(users_thirtytwo_algo[8:32])]

#Ethereum data
users_eight_eth  = [33.92665910720825, 46.30302882194519, 21.141716957092285, 14.177980184555054, 23.55874490737915, 23.877101182937622, 26.63273000717163, 21.890203952789307]
users_sixteen_eth = [41.73040699958801, 23.63556408882141, 24.96752905845642, 23.650923013687134, 20.642780303955078, 24.86896586418152, 28.924726009368896, 31.930116891860962, 35.00912380218506, 24.256208181381226, 40.97240900993347, 42.03148698806763, 25.359613180160522, 47.98902106285095, 36.17629599571228, 21.97417974472046]
users_twentyfour_eth = [54.689167976379395, 23.829805850982666, 36.86060190200806, 35.94429087638855, 24.923401832580566, 63.56628704071045, 55.611682176589966, 22.89153289794922, 48.8481228351593, 40.087875843048096, 48.201329708099365, 45.43669676780701, 22.646716833114624, 38.43727421760559, 45.618704080581665, 25.26260209083557, 19.59196710586548, 26.009806871414185, 35.91975712776184, 23.431020975112915, 23.433108806610107, 23.59810209274292, 23.436114072799683, 12.88370680809021]
users_thirtytwo_eth = [43.753134965896606, 34.98426413536072, 27.527480840682983, 33.03931903839111, 28.356040000915527, 70.83708429336548, 79.80655288696289, 78.10249781608582, 39.71377515792847, 46.900352001190186, 50.80634093284607, 33.216257095336914, 42.06699800491333, 24.92348623275757, 35.578798055648804, 48.42829918861389, 51.75394296646118, 51.116426944732666, 52.80358386039734, 32.85739779472351, 43.76271104812622, 52.43376326560974, 35.713481187820435, 47.050615072250366, 38.541098833084106, 58.13844704627991, 49.96871590614319, 29.836803913116455, 39.87191081047058, 35.0794141292572, 23.160690784454346, 49.71011710166931]


deployEthMean = [np.mean(users_eight_eth[0:2]),np.mean(users_sixteen_eth[0:4]),np.mean(users_twentyfour_eth[0:6]),np.mean(users_thirtytwo_eth[0:8])]
attachEthMean = [np.mean(users_eight_eth[2:8]),np.mean(users_sixteen_eth[4:16]),np.mean(users_twentyfour_eth[6:24]),np.mean(users_thirtytwo_eth[8:32])]


#Polygon data
users_eight_poly = [19.954870223999023, 19.225346088409424, 13.668169975280762, 13.521977186203003, 15.217917203903198, 15.608943939208984, 12.923369884490967, 14.43088412284851]
users_sixteen_poly = [21.139129161834717, 22.503053188323975, 18.941962957382202, 18.472630977630615, 12.233311891555786, 12.814027070999146, 12.999716997146606, 22.455791234970093, 40.85997700691223, 17.962791919708252, 19.085657835006714, 13.799613952636719, 18.24357795715332, 35.04382681846619, 18.378623008728027, 13.942615985870361]
users_twentyfour_poly = [19.683188915252686, 19.120874166488647, 21.800737142562866, 17.816470861434937, 19.965195894241333, 20.196632623672485, 37.688955307006836, 30.119228839874268, 28.94161605834961, 18.04338312149048, 28.018038988113403, 33.507181882858276, 33.907816886901855, 20.257228136062622, 18.91071105003357, 35.226516246795654, 34.756088972091675, 24.08308696746826, 14.329358100891113, 29.45211696624756, 42.398858070373535, 22.637013912200928, 15.81230115890503, 11.960737943649292]
users_thirtytwo_poly = [20.258759021759033, 19.921207904815674, 19.985855102539062, 22.198008060455322, 17.03529691696167, 27.17050004005432, 78.72941064834595, 25.43705701828003, 48.96301484107971, 53.60033583641052, 18.77692484855652, 38.661540269851685, 61.61586403846741, 20.608460187911987, 35.374865770339966, 54.83043694496155, 27.072927951812744, 25.208566904067993, 43.324995040893555, 32.53973197937012, 21.245217084884644, 31.936488151550293, 42.916419982910156, 40.74250388145447, 25.021095752716064, 51.7916259765625, 30.32864809036255, 27.513876914978027, 24.45020890235901, 26.165196180343628, 20.952993869781494, 14.751885890960693]

deployPolyMean = [np.mean(users_eight_poly[0:2]),np.mean(users_sixteen_poly[0:4]),np.mean(users_twentyfour_poly[0:6]),np.mean(users_thirtytwo_poly[0:8])]
attachPolyMean = [np.mean(users_eight_poly[2:8]),np.mean(users_sixteen_poly[4:16]),np.mean(users_twentyfour_poly[6:24]),np.mean(users_thirtytwo_poly[8:32])]


# plot lines DEPLOY
#Algorand Line
plt.plot(numberUsersTested, deployAlgoMean, label = "Algorand")
# Make the shaded area show the standard deviation
M_new_vec = np.array(deployAlgoMean)
Sigma_new_vec = np.array([np.std(users_eight_algo[0:2]),np.std(users_sixteen_algo[0:4]),np.std(users_twentyfour_algo[0:6]),np.std(users_thirtytwo_algo[0:8])])

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)

#Ethereum Line
plt.plot(numberUsersTested, deployEthMean, label = "Ethereum (Goerli)")
# Make the shaded area show the standard deviation
M_new_vec = np.array(deployEthMean)

Sigma_new_vec = np.array([np.std(users_eight_eth[0:2]),np.std(users_sixteen_eth[0:4]),np.std(users_twentyfour_eth[0:6]),np.std(users_thirtytwo_eth[0:8])])

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)

#Polygon Line
plt.plot(numberUsersTested, deployPolyMean, label = "Polygon")
# Make the shaded area show the standard deviation
M_new_vec = np.array(deployPolyMean)
Sigma_new_vec = np.array([np.std(users_eight_poly[0:2]),np.std(users_sixteen_poly[0:4]),np.std(users_twentyfour_poly[0:6]),np.std(users_thirtytwo_poly[0:8])]) 

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)

plt.legend()
plt.title('Deploy mean values')
plt.xlabel('Number of test')
plt.ylabel('Latency')  
plt.show()
plt.figure()
####################### END PLOT LINES DEPLOY #######################
#####################################################################

# ========================================================================================

#####################################################################
####################### PLOT LINES ATTACH ##########################
# plot lines ATTACH
#Algorand Line
plt.plot(numberUsersTested, attachAlgoMean, label = "Algorand")
# Make the shaded area show the standard deviation
M_new_vec = np.array(attachAlgoMean)
Sigma_new_vec = np.array([np.std(users_eight_algo[2:8]),np.std(users_sixteen_algo[4:16]),np.std(users_twentyfour_algo[6:24]),np.std(users_thirtytwo_algo[8:32])])

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)

#Ethereum Line
plt.plot(numberUsersTested, attachEthMean, label = "Ethereum (Goerli)")
# Make the shaded area show the standard deviation
M_new_vec = np.array(attachEthMean)
Sigma_new_vec = np.array([np.std(users_eight_eth[2:8]),np.std(users_sixteen_eth[4:16]),np.std(users_twentyfour_eth[6:24]),np.std(users_thirtytwo_eth[8:32])])

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)

#Polygon Line
plt.plot(numberUsersTested, attachPolyMean, label = "Polygon")
# Make the shaded area show the standard deviation
M_new_vec = np.array(attachPolyMean)
Sigma_new_vec = np.array([np.std(users_eight_poly[2:8]),np.std(users_sixteen_poly[4:16]),np.std(users_twentyfour_poly[6:24]),np.std(users_thirtytwo_poly[8:32])]) 

lower_bound = M_new_vec - Sigma_new_vec
upper_bound = M_new_vec + Sigma_new_vec

plt.fill_between(numberUsersTested, lower_bound, upper_bound, alpha=.3)



plt.legend()
plt.title('Attach mean values')
plt.xlabel('Number of test')
plt.ylabel('Latency')  
plt.show()
#####################################################################
####################### END PLOT LINES ATTACH #######################


# Deploy plot boxplot
dict_valuesBoxPlot = {'Algorand': users_thirtytwo_algo[0:8], 'Goerli': users_thirtytwo_eth[0:8], 'Polygon':users_thirtytwo_poly[0:8]}

fig, ax = plt.subplots()
ax.boxplot(dict_valuesBoxPlot.values())
ax.set_xticklabels(dict_valuesBoxPlot.keys())
ax.set_title("Deploy box plot")
plt.show()


# Attach plot boxplot
dict_valuesBoxPlot = {'Algorand': users_thirtytwo_algo[8:32], 'Goerli': users_thirtytwo_eth[8:32], 'Polygon':users_thirtytwo_eth[8:32]}

fig, ax = plt.subplots()
ax.boxplot(dict_valuesBoxPlot.values())
ax.set_xticklabels(dict_valuesBoxPlot.keys())
ax.set_title("Attach box plot")
plt.show()