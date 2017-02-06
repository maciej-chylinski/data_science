#Ustawiam workspace
#...

#wczytuję plik
air_quality <- read.delim("AirQualityUCI.csv", sep = ";", stringsAsFactors = FALSE, header = TRUE, na.strings = "")
#próbka danych
head(air_quality)

#instalacja pakietu ggplot
install.packages("ggplot2")
require(ggplot2)

#wykres wizualizujący zależności między odczytami x=NOx.GT.i y=NO2.GT.
ggplot(air_quality,aes(x=NOx.GT.,y=NO2.GT.))+geom_point()

#wykres wizualizujący zależności między odczytami x=NOx.GT.i y=NO2.GT.przy CO_level wprowadzonym do pliku ręcznie jako dodatkowa zmienna
ggplot(air_quality,aes(x=NOx.GT.,y=NO2.GT.))+geom_point(aes(colour=factor(CO_level),size=4))

