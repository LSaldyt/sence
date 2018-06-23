(ns sence.maze
  (:require [sence.astar :refer [astar]]
            [clojure.string :as str]))

(def toy-maze-string
"....
..0.
.00.
....")

(def toy-maze { 
  [0 0] [[0 1] [1 0]]
  [0 1] [[0 2] [0 0] [1 0]]
  [0 2] [[0 3] [1 3] [1 2] [0 1]]
  [0 3] [[1 3] [0 2] [1 2]] 
  [1 0] [[0 0] [0 1] [2 0]]
  [1 2] [[0 3] [1 3] [2 3] [0 2] [0 1]]
  [1 3] [[0 3] [2 3] [1 2] [0 2]]
  [2 0] [[1 0] [3 1] [3 0]]
  [2 3] [[1 3] [1 2] [3 3] [3 2]]
  [3 0] [[2 0] [3 1]]
  [3 1] [[2 0] [3 2] [3 0]]
  [3 2] [[3 3] [2 3] [3 1]]
  [3 3] [[2 3] [3 2]]
  })

(defn branches [node]
  (toy-maze node))

(defmacro ford [bind expression]
  `(into {} (for ~bind ~expression)))

(defn free? [space]
  (= space \.))

(defn maze-dict [maze-string]
  (let [maze-lines (str/split maze-string #"\n")]
    (ford [[y line] (map-indexed vector maze-lines)
           [x c]    (map-indexed vector line)
           :when (free? c)]
      [[x y] c])))

(defn parse-maze [maze-string]
  (let [maze (maze-dict maze-string)]
    (ford [[[x y] v] maze]
      [[x y] 
       (for [point [[(+ 1 x) y] [x (+ 1 y)]
                    [(- x 1) y] [x (- y 1)]]
             :when (contains? maze point)]
         point)])))

(println (parse-maze toy-maze-string))
(def toy-maze (parse-maze toy-maze-string))
(defn branches [node]
  (toy-maze node))
