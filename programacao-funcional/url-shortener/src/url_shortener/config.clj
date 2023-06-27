(ns url-shortener.config
  (:require [url-shortener.usecases :as uc]
            [url-shortener.datomicadapter :as dt]))

(defn
  hash-url-and-save
  [url]
  (uc/hash-url-and-save dt/save-to-datomic url))

(defn
  get-original-url
  [url]
  (uc/get-original-url dt/get-from-datomic url))