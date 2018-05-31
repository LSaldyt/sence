(ns ari.basics_test
  (:require [clojure.test :refer :all]
            [ari.core :refer :all]
            [ari.parse.parse :refer :all]
            [ari.parse.base :refer :all]))

;TODO: macros unifying common testing patterns

(def start-log {:head [] :verbosity 100})

(def test-tokens [["a" "name"] ["|" "pipe"] ["b" "name"]])

(defn full-tree [answer]
  (not (nil? (first answer))))

(deftest sep-test
  (testing "sepby"
    (is (= 2 (count (:values (first
      ((sep-by (tag "name" :name) (token "|"))
               test-tokens
               start-log))))))
    (is (nil? (first 
      ((sep-by1 (tag "name" :name) (token "|"))
       [["a" "name"]]
       start-log))))
    (is (= 2 (count (:values (first
      ((sep-by1 (tag "name" :name) (token "|"))
               test-tokens
               start-log
               ))))))))

(def conseq-parsers [(token "a" :a)
                     (token "|" :pipe)
                     (token "b" :b)])

(deftest conseq-test
  (testing "conseq"
    (is (full-tree
      ((conseq-merge conseq-parsers)
       test-tokens
       start-log)))))
    (is (full-tree
      ((conseq conseq-parsers)
       test-tokens
       start-log)))

(defparser n-parser (tag "N"))
(defparser p-parser (tag "P"))

(deftest from-test
  (testing "from"
    (is (full-tree
      ((from-except [n-parser] [p-parser])
       [["N" "N"]]
       start-log)))
    (is (nil? (first 
      ((from-except [n-parser] [n-parser])
       [["N" "N"]]
       start-log))))
    (is (full-tree
      ((from [(tag "NAH") (tag "name")])
       [["x" "name"]]
       start-log)))))

(deftest many-test
  (testing "many"
    (is (full-tree
          ((many (tag "name"))
           [["x" "name"]["x" "name"]]
          start-log)))
    (is (full-tree
          ((many (tag "x"))
           []
          start-log)))
    (is (full-tree
          ((many1 (tag "name"))
           [["x" "name"]["x" "name"]]
          start-log)))
    (is (not (full-tree
          ((many1 (tag "x"))
           []
          start-log))))))

(deftest optional-test
  (testing "optional"
    (is (full-tree
          ((optional (tag "x"))
           []
           start-log)))
    (is (full-tree
          ((optional (tag "x"))
           [["x" "x"]]
           start-log)))))

(deftest discard-test
  (testing "discard"
    (is (full-tree
          ((discard (tag "x"))
           [["x" "x"]]
           start-log)))
    (is (not (full-tree
          ((discard (tag "x"))
           []
           start-log))))))

(def parser-tree (atom {:ref (tag "x")}))

(deftest retrieve-test
  (testing "retrieve"
    (is (full-tree
          ((retrieve :ref parser-tree)
           [["x" "x"]]
           start-log)))
    (is (not (full-tree
          ((retrieve :ref parser-tree)
           []
           start-log))))))

; Test status
; x conseq 
; x conseq-merge 
; x many 
; x many1
; x from
; x from-except
; x optional
; x discard
; x sepby
; x sepby1
; x retrieve

