(ns interpid_explorer)
(require '[clojure.string :as string])

;; Read Maze File
(def matrix [])
(def file (line-seq (clojure.java.io/reader "map2.txt")))
(def file (map #(string/split % #"") file))
(def matrix (into matrix file))


(def len_column (- (count (first matrix)) 1))
(def len_row (- (count matrix) 1))
(def visited []) ;; An array to contain already visited cells
(def invalid_paths [])
(def maze matrix)

;; retrieve element in particular row and col
(defn retrieve [matrix row col]
  (get-in matrix[row col]))

;; check all axis for valid escape routes
(defn check_axis [matrix, row, col]
  (cond 
      (or (< row 0) (< col 0) (> row len_row) (> col len_column)) false
      (= (retrieve matrix row col) "#") false
      (some #(= (list row col) %) visited) false
      (some #(= (list row col) %) invalid_paths) false
      (= (retrieve matrix row col) "-") true
      (= (retrieve matrix row col) "@") true
  )
)

(defn findexit [matrix row col]

(def r (atom row))
(def c (atom col))
(def found? (atom true))

(defn recursive []
  (while (not= (retrieve matrix @r @c) "@")
    (do
        (cond
        (check_axis matrix @r (dec @c)) ( do (def maze (conj (assoc-in maze [@r @c] "+"))) (reset! c (dec @c)) (def visited (conj visited (list @r @c))) )
        (check_axis matrix (inc @r) @c) ( do (def maze (conj (assoc-in maze [@r @c] "+"))) (reset! r (inc @r)) (def visited (conj visited (list @r @c))) )
        (check_axis matrix @r (inc @c)) ( do (def maze (conj (assoc-in maze [@r @c] "+"))) (reset! c (inc @c)) (def visited (conj visited (list @r @c))) )
        (check_axis matrix (dec @r) @c) ( do (def maze (conj (assoc-in maze [@r @c] "+"))) (reset! r (dec @r)) (def visited (conj visited (list @r @c))) )
        
        :else (do 
                  (if (= (count visited) 1)
                  (do (println "\n Uh oh, I could not find the treasure :-( \n\n") (def maze (conj (assoc-in maze [(nth (last visited) 0) (nth (last visited) 1)] "!")))(reset! found? false) (run! #(println (string/join "" %)) maze) (System/exit 0))
                    ;; lets backtrack
                  (if (> (count visited) 1)
                    (do
                      (def invalid_paths (conj invalid_paths (last visited))) 
                      (def visited (pop visited))
                      (
                        
                        do 
                        (def last_valid_path (last visited))
                        (def maze (conj (assoc-in maze [@r @c] "!")))
                        (reset! r (nth last_valid_path 0) ) 
                        
                        (reset! c (nth last_valid_path 1))
                        
                      
                      )
                      
                    )
                  )
                  ) 
              )

        )
    )
  )
)

(recursive)
  (if @found?
  (println "\n\n Woo hoo, I found the treasure :-) \n")
  )
)

(println "This is my challenge: \n")
(def unsolved_map (slurp "map.txt"))
(println unsolved_map)
(findexit matrix 0 0)

(run! #(println (string/join "" %)) maze)
