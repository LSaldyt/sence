(ns sence.astar)

(defn astar 
  ([branches, start, end, distance] (astar branches start end distance 
                                     {start [start]} #{}))
  ([branches, current, end, distance, paths, seen]
;    branches is a function:
;    branches(key, end) -> connected nodes
;    start is a syntax element
;    end is the desired list
;    distance is a heuristic function:
;    dist(current, end) -> num
   ;(println "Current node:")
   ;(println current)
   ;(println "Distance")
   ;(println (distance current end))
   (defn complexity [node] (count (paths node)))
   (defn heuristic [node] 
     (+ (complexity node) (distance node end)))
   (if (= current end)
     (paths current)
     (loop [neighbors (branches current)
            inner-paths paths]
       (if (empty? neighbors)
           (astar branches (apply min-key heuristic (keys inner-paths))
                  end distance (dissoc inner-paths current) (conj seen current))
           (let [item (first neighbors)]
             ;(println "Item:")
             ;(println item) 
             (recur (rest neighbors)
                (if (and (or (not (contains? inner-paths item)) 
                             (> (complexity item) (+ (complexity current) 1)))
                         (not (contains? seen item)))
                   (assoc inner-paths item (conj (inner-paths current) item))
                   inner-paths))))))))
