(ns sence.core
  "Translation script / effective test"
  (:require [clojure.tools.cli :refer [cli]]
            [clojure.math.numeric-tower :refer :all]
            [sence.maze :refer :all]
            [sence.astar :refer :all])
  (:gen-class))


(defn -main [& in-args]
  (let [[opts args banner] (cli in-args
    ["-h" "--help" "Print this help"
     :default false :flag true])]
    (when (:help opts)
      (println banner))
    (println astar)
    (defn distance [[ax ay] [bx by]]
      (sqrt (+ (abs (- ax bx)) (abs (- ay by)))))
    (println (astar branches [0 3] [3 0] distance))
    ;([branches, start, end, distance] (astar branches start end distance 
    ))
