# Coordenadas de los puntos
x <- c(-1, 2, 4, 2, -1, 1)
y <- c(2, 3, 2, 1, -2, 1)

# Nombres de los puntos
nombres <- c("A", "B", "C", "D", "E", "F")

# Crear data frame
puntos <- data.frame(x, y, row.names = nombres)
puntos

# Graficar los puntos en el plano
plot(puntos, xlim = c(-3, 6), ylim = c(-3, 6))
text(puntos, labels = nombres, pos = 1)

# Calcular matriz de distancias euclidianas
puntos.dist <- dist(puntos, method = "euclidean")
puntos.dist

# --- Método del vecino más cercano (Single Linkage) ---
puntos.hc <- hclust(puntos.dist, method = "single")
plot(puntos.hc, cex = 0.5, hang = -0.1, axes = TRUE)
abline(h = 2.1, lty = 2)

# --- Método del vecino más lejano (Complete Linkage) ---
puntos.hc1 <- hclust(puntos.dist, method = "complete")
plot(puntos.hc1, cex = 0.6, hang = -0.1, axes = TRUE)
abline(h = 2.1, lty = 2)

# Formar clusterse usando el metoso ward.D

puntos.hc2 <- hclust(puntos.dist,"ward.D")
plot(puntos.hc2, cex = 0.6, hang = -0.1, axes=T)
abline(h=2.1,lty=2)

# Formar clusters usando el método del centroide

puntos.hc3<- hclust(puntos.dist, method = "centroid")
plot(puntos.hc3,cex = 0.6, hang = -0.1, axes = TRUE)
abline(h = 2.1, lty = 2)
