(ns url-shortener.config
  (:require [url-shortener.usecases :as uc]
            [url-shortener.datomicadapter :as dt]))

(defn
  hash-and-save-url
  "Hashes the given URL and saves it to Datomic."
  [url]
  (try
    (uc/hash-url-and-save dt/save-to-datomic url)
    (catch Exception e
      (println "An error occurred while hashing and saving the URL: " (.getMessage e)))))

(defn
  get-original-url
  "Retrieves the original URL from Datomic using the hashed URL."
  [url]
  (try
    (uc/get-original-url dt/get-from-datomic url)
    (catch Exception e
      (println "An error occurred while retrieving the original URL: " (.getMessage e)))))
