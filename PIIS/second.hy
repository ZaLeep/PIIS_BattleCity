(import [random :as rd])

(defn rand_map [map]
    (for [i (range 5)]
        (for [j (range 5)]
            (if (or (and (= i 0) (= j 2)) (and (= i 3) (= j 2)))
            (setv (get (get map i) j) 2)
            (setv (get (get map i) j) (rd.randint 0 1))
            )
        )
    )
)

(setv map [[0 0 0 0 0] [0 0 0 0 0] [0 0 0 0 0] [0 0 0 0 0] [0 0 0 0 0]])
(rand_map map)
(for [i (range 5)]
(print (get map i)))