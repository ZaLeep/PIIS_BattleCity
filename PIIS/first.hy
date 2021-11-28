(import [pandas :as pd])
(import [numpy :as np])


(defn math_expecting [arr]
    (setv sum 0)
    (setv i 0)
    (for [x arr]
        (setv sum (+ sum x))
        (setv i (+ i 1)))
    (/ sum i))

(defn dispersion [arr exp]
    (setv sum 0)
    (setv i 0)
    (for [x arr]
        (setv sum (+ sum (** (- x exp) 2)))
        (setv i (+ i 1)))
    (/ sum i))

(setv col ["result" "hp" "kill" "map" "time" "score" "algh"])
(setv res (pd.read_csv "result.csv" :usecols col))
(setv for_expect (np.array res.time))
(setv for_disp (np.array res.score))
 
(print "Expecting value of time:" (math_expecting for_expect))
(print "Expecting value of score:" (math_expecting for_disp))
(print "Dispersion:" (dispersion for_disp (math_expecting for_disp)))