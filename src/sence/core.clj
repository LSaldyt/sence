(ns sence.core
  "Translation script / effective test"
  (:require [clojure.tools.cli :refer [cli]]
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
    ))
