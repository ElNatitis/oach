library(cluster)
library(purrr)

datos <- carData::Freedman

# se eliminan los valores perdidos de los datos

datos <- na.omit(datos)
# Se escalan los datos de las variables numéricas, esto 
# significa que cada variable ahora tendrá una media cero
# y una desviación estándar uno. 
# Lo ideal es que quieras que cada variable tenga la misma unidad de escala,
# de modo que una unidad en cada coordenada represente la misma magnitud de diferencia.
# Escalar evita que el algoritmo de agrupamiento dependa de una unidad arbitraria.
# Puedes escalar los datos usando la función scale():
# ---------------------------------------------------------
datos <- scale(datos)

# ---------------------------------------------------------
# medidas de similitud: distancias
# comandos: dist() y get_dist()
# ---------------------------------------------------------
# 
# calculando las distancias con el método seleccionado.
# Por default, se usa la distancia euclidiana.
# ---------------------------------------------------------

# Distancia Euclidiana
d1 <- dist(datos, method = "euclidean")

# Redondear la matriz de distancias (primeras 4 filas y columnas)
round(as.matrix(d1)[1:4, 1:4], 2)

# Visualizar la matriz completa en una ventana aparte
View(round(as.matrix(d1)[1:4, 1:4], 2))

# Distancia de tipo "máximo" (Chebyshev)
d2 <- dist(datos, method = "maximum")
round(as.matrix(d2)[1:4, 1:4], 2)


d3 <- dist(datos, method = "manhattan")
round(as.matrix(d3)[1:4, 1:4], 2)

d4 <- dist(datos, method = "canberra")
round(as.matrix(d4)[1:4, 1:4], 2)

d5 <- dist(datos, method = "minkowski",p=4)
round(as.matrix(d5)[1:4, 1:4], 2)

library(StatMatch)
# Cálculo de la distancia de Mahalanobis
d6 <- mahalanobis.dist(data.x = datos)

# Convertir el resultado a objeto tipo "dist"
d6 <- as.dist(d6)

# Mostrar las primeras 4 filas y columnas redondeadas
round(as.matrix(d6)[1:4, 1:4], 2)


# La distancia de Mahalabous no necesita que se escalen los datos, ya que da el mismo resultado, en cambio las otras distancias si cambian su resultado

datos.2 <- carData::Freedman
datos.2 <- na.omit(datos.2)

d6.a <- mahalanobis.dist(data.x=datos.2)
d6.a <- as.dist(d6.a)
round(as.matrix(d6.a)[1:4,1:4],2)

# ---------------------------------------------------------
# Coeficiente de correlación 
library(factoextra)
