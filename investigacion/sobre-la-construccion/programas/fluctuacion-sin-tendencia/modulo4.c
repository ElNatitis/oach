/* MODULO 4 - CALCULAR LA FLUCTUACIÓN CUADRÁTICA MEDIA

Se reciben los arreglos un
 - 'seg_instrumento_int' 
 - 'sim_seg_instrumento'
que comparten la siguiente estructura la siguiente estructura:
  { [(d1,...,ds)₁,...,()], [(),...,()ₙ], [()₁,...,(d_int)ₙ] }

y se realizan los siguientes procedimientos

1 - para cada segmento, se suman las diferecnias al cuadrado de los i-ésimos términos de 'seg_instrumento_int' y ' sim_seg_instrumento'
2 - se suman esas sumas en una variable llamada F
3 - se calcula la fcm (dividimos F entre st*s y le sacamos raíz cuadrada)

El programa regresa un arreglo con el formato

f_s = { [s], [F_t,F_v,F_d] }

donde
  s := tamaño de los segementos
  F_ := "magnitud promedio de fluctuaciones" de tono, volumen y duración con respecto a ese tamaño de segmento
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"

float diff(float* x_seg, float* x_seg_sim, int s);

float* fluctuaciones(struct instrumento inst, struct instrumento inst_sim, int s)
{
  int st = ((N-(N%s))/s); // número de segmentos que habrá en el arreglo de segmentos
  float s_t = 0, s_v = 0, s_d = 0;
  for(int i=0;i<st;i++)
  {
    // apuntadores para cada segmento real
    float* seg_tono = inst.tono+i*s;
    float* seg_volumen = inst.volumen+i*s;
    float* seg_duracion = inst.duracion+i*s;
    
    // apuntadores para cada segmento simulado
    float* seg_sim_tono = inst_sim.tono+i*s;
    float* seg_sim_volumen = inst_sim.volumen+i*s;
    float* seg_sim_duracion = inst_sim.duracion+i*s;
    
    // calculamos las diferencias al cuadrado
    float diff_tono = diff(seg_tono, seg_sim_tono, s);
    float diff_volumen = diff(seg_volumen, seg_sim_volumen, s);
    float diff_duracion = diff(seg_duracion, seg_sim_duracion, s);
    
    // sumamos cada resultado
    s_t += diff_tono;
    s_v += diff_volumen;
    s_d += diff_duracion;
  }
  
  float* fcm = calloc(4, sizeof(float));
  fcm[0] = s;
  fcm[1] = sqrt(s_t / (st * s));
  fcm[2] = sqrt(s_v / (st * s));
  fcm[3] = sqrt(s_d / (st * s));

  printf("para segmentos de %.2f elementos tenemos las siguientes magnitudes promedio de fluctuaciones \n\tf_tono = %f \n\tf_volumen = %f \n\tf_duraciones = %f\n",fcm[0],fcm[1],fcm[2],fcm[3]);
  return fcm;

}


float diff(float* x_seg, float* x_seg_sim, int s)
{
  float sum=0,resta;
  for(int i=0;i<s;i++)
  {
    resta = x_seg[i] - x_seg_sim[i];
    sum += resta*resta;
  }
  return sum;
}
