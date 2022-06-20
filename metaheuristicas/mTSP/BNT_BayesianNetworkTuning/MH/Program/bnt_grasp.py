
import argparse
import logging
import time
from grasp import GRASP 
from instances import import_instance


def main(arquivo, GRASP_max, RLC_length_in_percentage, alpha_min, alpha_max):
    inicio = time.time()
    instance = import_instance(arquivo)    
    fo = GRASP(instance, GRASP_max, RLC_length_in_percentage, alpha_min, alpha_max)
    final = time.time()
    tempo_total = final - inicio
    print("Result for BNT: Solved, %.4f, 0, %.2f, 0" % (tempo_total, fo))

if __name__ == "__main__":    
    ap = argparse.ArgumentParser(description='Calibracao de parametros GRASP')
    ap.add_argument('instancia', type=str, help='Instancia em teste')
    ap.add_argument('-GRASP_max', dest='GRASP_max', type=int, required=True)
    ap.add_argument('-RLC_length_in_percentage', dest='RLC_length_in_percentage', type=int, required=True)
    ap.add_argument('-alpha_min', dest='alpha_min', type=int, required=True)
    ap.add_argument('-alpha_max', dest='alpha_max', type=int, required=True)
    args = ap.parse_args()
    logging.debug(args)
    main(args.instancia, args.GRASP_max, args.RLC_length_in_percentage, args.alpha_min, args.alpha_max)

# No Windows
# python Main.py MH/Instances/mTSP/mtsp51_3.txt -MAX_GRASP 100 -ALPHA_GRASP 5