(ns sence.core
  "Translation script / effective test"
  (:require [clojure.tools.cli :refer [cli]])
  (:gen-class))


(defn -main [& in-args]
  (let [[opts args banner] (cli in-args
    ["-h" "--help" "Print this help"
     :default false :flag true])]
    (when (:help opts)
      (println banner))

    ))
