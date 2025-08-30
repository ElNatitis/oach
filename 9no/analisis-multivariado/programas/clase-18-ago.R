
# Declaramos la variable que contiene la base de datos
bddieta <- read.table(file='dieta.csv',
			header = TRUE,
			sep = ';',
			dec = '.',
			encoding = 'UTF-8',
			stringsAsFactors = FALSE)

# Oservamos las primeras 4 filas de nuestra base de datos
head(bddieta,4)

str(bddieta)

tail(bddieta,2)

# Se tienen que conversitr las variables categoricas o cualitaticvasm en este caso, las variables tipoDiet y edad aparecen tipo int hayq ue transformarlas a factor para que R reonoxca sus calores como nicveles de una variable categhorica

bddieta$tipoDiet <- factor(bddieta$tipoDiet)
bddieta$edad <- factor(bddieta$edad)

str(bddieta)

# Ejercicio:
# Comprubea si hay diferencias en la media de los pesos antes de comenzar la dieta (variable peso 0) según el grupo de edad al que pertenece y encuentra en qué grupos están las diferencias.

# Se va a realizar un ANOVA de una via (factror entre sujetos, ya que varia entre los sujetos y el factor se mide solo una vcez para un mismo sujeto), paRA COMPARAR LAS MEDIES, EN ESTE CASO TENEMOS TRES MEDIAS PARA COMPARAR QUE CORRESPONDEN A LOS TRES GRUPOS DE ESDA

# Variable depenidente (VD) = peso , cariable cuanitiativa
# Factor (Variable indepoendiente) = edad cariable categprica de 3 niverlees


# PAra u ANOVA de una vai se debe comprobar el suúesto de indepéndendia, es supuesto de normalidad y el supuesto de homocedasticidsad

# supuesto de independencia de las observaciones: se suipione la independencia de las observaciones cuando se aplica muestreo aleatorio

# supuesto de normalidad: realizar el contraste para normalidad. En este constraste la hipotesis nula es la hipotesis de normalidad, esto es, no hay diferencias entre nuestra distribucion yu una distribucion normal con esa media y esa desviacion típica. PAra contrastar lanhoramlidad usamior el test shapiro-wilkm con una funcoin shapiro.test() qu efunciona biuen con muiestras pequeñas, mnenores a 50

# aplcianod shapiro test

#individual 
shapiro.test(bddieta$peso0[bddieta$edad == '1'])
shapiro.test(bddieta$peso0[bddieta$edad == '2'])
shapiro.test(bddieta$peso0[bddieta$edad == '3'])

# para hacerlo automatico con todos los grupos
by(data=bddieta, INDICES=bddieta$edad,FUN=function(x){shapiro.test(x$peso0)})

# Para todos los grupos de edad se obtiene un p-value mayuor de 0.5 dsjdasijsa



# Supuesto de homocedasticidad: Es la homogeniedad de la varianza de la variable dependiente entre los grupos. En el contraste de homogeneidad de varianzasz la hipotesis nula es: la varianza es constraste (no varia= en los diferentes grupos. PAra constrastarla utilizamos el test de Bartlett con bartlett.test(), qu es más robusto que otros test cuando los datos son normales.

bartlett.test(peso0 ~  edad, data = bddieta)

# por el valor de p value no podemos recharat la hiopoteis nula, Por lo tanto suponemos homogeneidad de varianzas

#####################################

# Enel ANOVA de una via la hipotesius nula h0 es que nno hay diferencias entre las medias y la hipotesis alternativa h1 es que al menos una de las las medias idifiere del resto. En nuestro caso, siu el peso ed cada individuo 


#EL modelo ANOVA contrasta las diferencias en las medias en el peso entre los dujetos egun el grupo de edad

modelo1 <- aov(peso0 ~ edad, data = bddieta)
summary(modelo1)

# con p-vlaue qu etenemos que es menor de 0.5 podemos rechazar la hipotesis nula. Se rechaza la hipotesis nula y "aceptamos la hipotesis alternativa" de que hay diferencia enalmenos una de las media de los grupos de edad. Es decir, la edad tiene un efecti significativo en el peso inicial.

####
# Contrastes post-hoc
####

# Para concoer ´qué grupo de edad son los que difieren' se deben realizar contrastes dos a dos corerigiendo el nivel de significacion. EL procedimeinto post-hoc constrasta las diferencias de todos los grupos e identifica aquellas diferencias que son estadisticametne significativas.

#REalizamos contrastes post-hoc o no pĺanificados(sin idea previa) con menos de 6 niveles (tenemos 3 grupos de edad) usamos el metodo de Bonferroni

#pairwise.t.test(bddieta$peso0, bddieta$edad, p.adj='bonferroni')

pairwise.t.test(bddieta$peso0,bddieta$edad,p.adj='bonferroni')

# Existen diferencias significativas (p-valor<0.05) ecntre:
# el grupo de edad 3 y el grupo de edad 1 ,
# el grupo de edad 3 y el grupo de edad 2
# y entre el grupio 1 y el 2 no existen diferencias
# significativas respecto a su peso inicial


#################### otro ejercicio

# Comprueba si hay diferencias significativas en el peso final (peso2) segun la interaccion del grupo de edad al que pertenece el dujeto y el tipo de dieta al que se somete.
# Representa el grafico de interacion con la edad en el ejex y el 'tipoDiet' en 3 lineas diferentes.

######################

# Aqui se va a realizar un ANOVA de dos vias, de dos factoresm, ya que analiza la igualdad de las medias de lapóbalcion para un resultado cuantitativo y dos variables categoricas o factores
# Entre sujetos: La variable edad se mide una vez en cada sujeto petenece a un solo grupo o nivel de variable 'tipoDiet'

# VD (resultado): peso2, vairbale cuantitativa
#Factores (VI) greupo de edad al que pertenece el sujeto (edad contres niveles) y el tipo de dieta al que se domete (tes niveles tmabien) variables categoricas

# Para ANOVA de dso vias se debe comprobar elsuṕuesto de independencia, el supeusto de normalidad y el supuesto de homocedasticidad. Estos supuestos se deben comprobar para le fator edad y para el factor tipoDiet. Esto es, se comprueba la normalidad para todos los niveles de cada factor, y se comprueba la homcedasticidad para ambos factores.


#........................
# comprobacion de supuestosx para el factor edad:

## supuesto de normalidad: usamos el test Shapiro-wilk, con la funcoin shapiro.test

by(data= bddieta,INDICES = bddieta$edad,FUN=function(x){shapiro.test(x$peso2)})

## supuesto de homocedaticidad: usamos el test de barlett que es mas robusto qyue otros cuando los datos on nomrelaes

bartlett.test(peso2~edad,data=bddieta)

#........................
# Comprobacion de supuestos para el factor tipoDiet

## supuesto de normalidad: test de Shapiro-wilk
by(data= bddieta,INDICES = bddieta$tipoDiet,FUN=function(x){shapiro.test(x$peso2)})

## supuesto de homocedasticidad test de barlett
bartlett.test(peso2~tipoDiet,data=bddieta)

#..........#
#Estimacion del modelo ANOVA

# el mopdelo ANOVA evalua, ademas de los efectos de los factores sobre la variable dependiente, los efectos dela interaccion entre ellas. La hipotesis nula es lo que no hay interaccion entre los factortes

# Si los datos son balanceados, no importa el irdebn de los dactoes en la fucnoin aov(). Est es, si ponemos dactor1 * factor2 io si ponemos factor 2* factor 1

#comprobamos si son balanceados nuestros datos mediante unas tablas de frecuencias absoluitas vemos que el numero de observaciones es el mismo para todos los niveles de cada factor, por tanot nuestros datos están balanceados

table(bddieta$edad)
table(bddieta$tipoDiet)

modelo2<-aov(peso2~edad*tipoDiet, data=bddieta)
summary(modelo2)

# La vartiable tipoDiet tiene un efecto significativo, la edad no, respecto a la interaccion se acepta la hipotesis nula, esto es, no hay interaccion entre ambas variables.

# por lo tanto, cconcuimos que no hay diferencias significativas en el peso final segun la itneraccion de la edad del grupo al que pertenece el sujeto y el tipo de dieta la que se somete

# efecto interaccoin:
# el termino reperesenta le efecto conjunto de ls dos factores. Con los resultado obtenido en el modelo ANOVA, hemos concluido que no hay diferencias significaticvas en el peso final segun la interaccion del grupo de esas al que pertenece el sujeto. La iunterpretacion de lainteraccion se describe mejor cisulamente, COn la fuincio interaction.plot() representamios el grapfico de interaccion: con aledad en el eje x y el tipoDIet en tres lienad idefernes
# LAvbariablñe dependietne PEso2 en el ejy 

interaction.plot(bddieta$edad,bddieta$tipoDiet,bddieta$peso2)
par('mar')
par(mar=c(6,4,2,2))


#.....................................
# ejercicio 3 
#............................................

## fotos en el celular jsjs

# se utiliza la funcoin melt() del paquete reshape2
#install.packages("reshape2")
library(reshape2)
bd.melt <- melt(bddieta,
		id = c('id','edad','tipoDiet'),
		measure = c('peso0','peso1','peso2'),
		variable.name = 'PesoPeriodo',
		value.name = 'PesoKg')
		
head(bd.melt)
tail(bd.melt)
str(bd.melt)

#............................................
# supuestos basicos de ANOVA MR

# Para un ANOVA para medidas repetidas se debe comprobar el supuesto de nromalidad y el supuesto es esfericidad

## supuesto de normalidad
# usamos el test de Shapiro-wilk, con la funcion shapiro.test()

by(data=bd.melt,INDICES=bd.melt$PesoPeriodo,FUN=function(x){shapiro.test(x$PesoKg)})

# EN todos los periodos en elq ue se mide el peso se obtiene un p-value mayor de 0.5m no podemos rtechazar la hipotesis de normalidad (nuña) por lo tanto podemos conlcuir que nuestros datos cumplen el supuessto de normalidad

# Para lo demas tomé una foto el dia 20 de agosto en mi celular

#...............
#ESTIMACION DEL MODELO ANOVA
# Realizamos el modelo ANOVa para medidas repetidas con la funcoin ezANOVVA(), del paquete ez:

#install.packages("devtools")

library(ez)

options(contrasts = c('contr.sum','contr.poly'))

ezANOVA(data = bd.melt,
	dv = PesoKg,
	wid=id,
	within = PesoPeriodo,
	type = 3)
