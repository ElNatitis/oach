# Detección "automática" de outliers

# Usando los datos de contaminacion 

data("USairpollution",package = "HSAUR2")
x<- USairpollution
cm <- colMeans(x)
S <- cov(x) 

# Distancia generalizada (Mahalenobis)
d <- apply(x,1, function(x) t(x-cm) %*% solve(S) %*% (x-cm) ) 


# se grafican los datos 
plot(qc<-qchisq((1:nrow(x)-1/2)/nrow(x),df=6),sd<-sort(d),
	xlab= expression(paste(chi[6]^2, "Quantline")),
	ylab= "Ordered distances", xlim=range(qc)*c(1,1.1))
	
	
# se identifican los outliers
oups<-which(rank(abs(qc-sd),ties="random")>nrow(x)-3)

# Se agregan los nombres en la gráfica
text(qc[oups],sd[oups]-1.0,names(oups))
abline(a=0,b=1)

#====================================================================================

library(MVA)
#etiquetas
mlab<- "Manufacturing Enterprises whit 20 or more workers"
plab<- "Population size (1970 census) in thousands"

outcity <- match(lab<-c("Chicago","Detroit","Cleveland","Philadelphia"),
		rownames(USairpollution))

x<- USairpollution[,c("manu","popul")]

# Con la grefica boxplot bivariada se pueden determinar valores átipicos 
par(mar=c(4,4,4,2))
bvbox(x,mtitle="",xlab=mlab,ylab=plab)
text(x$manu[outcity],x$popul[outcity],labels=lab,cex=0.7,pos=c(2,2,4,2,2))


#USairpollution

# Aqui se observan los posiubles valorea atípicos y aquellos qure quedan dentro o sobre la elipse no son considerados como valores atípicos 

# Observese como cambia el valor ede la corelación con y sin los valores atípicos destacados 
with(USairpollution,cor(manu,popul))
outcity <- match(c("Chicago","Detroit","Cleveland","Philadelphia"),rownames(USairpollution))
##### para hacer pruebas #####
#class(USairpollution)
#USairpollution$popul[-outcity]
#USairpollution$popul
#outcity
#cor(USairpollution$manu[-outcity],USairpollution$popul[-outcity])

with(USairpollution,cor(manu[-outcity],popul[-outcity]))



