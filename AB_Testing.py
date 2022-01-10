import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 80)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("Dersler/HAFTA5/Ders Notları/ab_testing.xlsx",sheet_name="Control Group")
df_test = pd.read_excel("Dersler/HAFTA5/Ders Notları/ab_testing.xlsx",sheet_name="Test Group")

df_test["Purchase"].mean() #582.1060966484675

df_control["Purchase"].mean() #550.8940587702316

########################################## Görev 1 #############################################
#A/B testinin hipotezini tanımlayınız.


#H0:e averagebidding’in satın alım ortalaması maximumbidding satın alım ortalamasına eşittir
#H1:..... eşit değildir

########################################## Görev 2 ############################################
#Hipotez testini gerçekleştiriniz. Çıkan sonuçların istatistiksel olarak anlamlı olup olmadığını yorumlayınız.


############## ADIM 1 : Hipotezi kur
#H0:e averagebidding’in satın alım ortalaması maximumbidding satın alım ortalamasına eşittir
#H1:..... eşit değildir

############## ADIM 2 : Varsayımları kontrol et

#1.Varsayım Normallik Testi:

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # H0 reddilemez,normaldir
test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))# H0 reddilemez,normaldir

#2.Varsayım Varyans homojenliği Testi:
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df_test["Purchase"],
                           df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #H0 reddedilemez,varyans homojenliği sağlanmaktadır

############## ADIM 3 : Varsayımlar sağlanıyor parametrik test uygula

#H0:averagebidding’in satın alım ortalaması maximumbidding satın alım ortalamasına eşittir
#H1:..... eşit değildir

test_stat, pvalue = ttest_ind(df_test["Purchase"],
                              df_control["Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#H0 reddedilemez. %95 güvenle averagebidding’in satın alım ortalaması
# maximumbidding satın alım ortalamasına eşittir.


########################################## Görev 3 ############################################
#Hangi testi kullandınız, sebeplerini belirtiniz.

#Normallik varsayımı sağlandığı için öncelikle parametrik teste gittim. orada argümana etki eden
#vryans homojenliği sağlandığı için equal_var'ı True yapıp bağımsız iki örneklmeler t testini uyguladım

########################################## Görev 3 ############################################
#Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

"""
Biz bu iki teklif vermeden birinin farklı olmasını isterdik ki şirketimiz artık o teklif vermeyi kullansın diye fakat
şuan ki sonuçlara bakacak olursak bir farklılık görünmediğini analiz ettik.
Bundan dolayı ortalamalardan fazla olan teklif verme türünü kullanabiliriz.
ya da şuan ikisi arasından fazla olan ortalamanın türünü kullanıp her ay bu analizi yapıp gözlemleyebiliriz.
diğer değişkenler bakımından testler yapıp hepsinin sonucunda bir aksiyon alabiliriz
*örneğin reklam görüntüleme sayısı/ yıklanma sayısı oranına bakıp 
bu oranlar arasında anlamlı bir farklılık var mı yok mu ya bakılabilir
*ortalama kazançları bakımından farklılar mı diye bakılabilir
"""

################################################ EK ANALİZLER #######################################

##############################
#### tıklanma/görüntülenme ####
##############################

df_control["p"]=df_control["Click"]/df_control["Impression"]
df_test["p"]=df_test["Click"]/df_test["Impression"]

############## ADIM 1 : Hipotezi kur
#H0:e averagebidding’in (tıklanma/görüntülenme) ORANI maximumbidding (tıklanma/görüntülenme) oranına eşittir
#H1:..... eşit değildir

############## ADIM 2 : Varsayımları kontrol et

#1.Varsayım Normallik Testi:

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df_test["p"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # H0 red,normal değil
test_stat, pvalue = shapiro(df_control["p"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))# H0 red,normal değil


############## ADIM 3 : Varsayımlar sağlanmıyor non parametrik test uygula

#H0:e averagebidding’in (tıklanma/görüntülenme) maximumbidding aynı oranına eşittir
#H1:..... eşit değildir

test_stat, pvalue = mannwhitneyu(df_test["p"].dropna(),
                                 df_control["p"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#H0 red. %95 güvenle averagebidding’in tıklanma oranının
# maximumbidding tıklanma oranına eşit değildir.

df_test["p"].describe().T  #%50 = 0.03136
df_control["p"].describe().T  #%50 = 0.04880

#buradan harketle maximum bidding seçilebilir


##############################
#### ortalama kazançlar ######
##############################


####ADIM 1 : Hipotezi kur
#H0:e averagebidding’in ortalama kazancı maximumbidding aortalam kazancına eşittir
#H1:..... eşit değildir

####ADIM 2 : Varsayımları kontrol et

#1.Varsayım Normallik Testi:

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # H0 reddilemez,normal
test_stat, pvalue = shapiro(df_control["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))# H0 reddilemez,normal


#2.Varsayım Varyans homojenliği Testi:
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df_test["Earning"],
                           df_control["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #H0 reddedilemez,varyans homojenliği sağlanmaktadır


##### ADIM 3 : Varsayımlar sağlanıyor parametrik test uygula

#H0:e averagebidding’in ortalama kazancı maximumbidding aortalam kazancına eşittir
#H1:..... eşit değildir

test_stat, pvalue = ttest_ind(df_test["Earning"],
                              df_control["Earning"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

##H0 red. %95 güvenleveragebidding’in ortalama kazancı maximumbidding aortalam kazancına eşit değildir.

df_test["Earning"].mean() #2514.8907326506173
df_control["Earning"].mean() #1908.5682998027492


