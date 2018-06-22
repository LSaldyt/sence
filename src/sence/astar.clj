(ns sence.astar)

;(defn heuristic [node])
(defn distance [node end])

(defn neighbors [node])

(defn check-neighbors [neighbors current open closed]
  (if (empty? neighbors) [open closed]
      (let [neighbor  (first neighbors)
            remaining (rest neighbors)]
        (if (contains? closed neighbor)
            (check-neighbors remaining current open closed)
            (if (not contains? open neighbor)
              (check-neighbors remaining 
                               (assoc open neighbor (conj (get open current) neighbor))
                               closed)
              ())))))

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
   (defn complexity [node] (count (paths node)))
   (defn heuristic [node] 
     (* (complexity node) (distance node end)))
   (if (= current end)
     (paths current)
     (let [shortest ()]
       (loop [neighbors (branches current)
              inner-paths paths]
         (if (empty? neighbors)
             (astar branches current end distance inner-paths (dissoc seen current)))
             (let [item (first neighbors)]
               (recur (rest neighbors)
                  (if (and (or (not (contains? paths)) 
                               (> (complexity (paths item)) (complexity item)))
                           (not (contains? seen item)))
                     (assoc paths item (conj (paths current) item))
                     paths))))))))

;    while tuple(end) not in paths:
;        seen.add(shortest)
;
;        for item in branches(paths[shortest], end):
;            l = item.complexity()
;            if (item not in paths or paths[item].complexity() > l) and \
;                to_seq(item) not in seen:
;                paths[to_seq(item)] = item
;        del paths[shortest]

;(defn a-star 
;  ([current, end] (a-star current end {current} {current []}))
;  ([current, end, open, closed]
;   (if (= current end)
;     (get closed current)
;     )))


;    while openSet is not empty
;        current := the node in openSet having the lowest fScore[] value
;
;        openSet.Remove(current)
;        closedSet.Add(current)
;
;        for each neighbor of current
;            if neighbor in closedSet
;                continue		// Ignore the neighbor which is already evaluated.
;
;            if neighbor not in openSet	// Discover a new node
;                openSet.Add(neighbor)
;            
;            // The distance from start to a neighbor.
;            // The "dist_between" function may vary as per the solution requirements.
;            tentative_gScore := gScore[current] + dist_between(current, neighbor)
;            if tentative_gScore >= gScore[neighbor]
;                continue		// This is not a better path.
;
;            // This path is the best until now. Record it!
;            cameFrom[neighbor] := current
;            gScore[neighbor] := tentative_gScore
;            fScore[neighbor] := gScore[neighbor] + heuristic_cost_estimate(neighbor, goal) 
;
;    return failure
