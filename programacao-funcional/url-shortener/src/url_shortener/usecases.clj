(ns url-shortener.usecases
  (:require
   [url-shortener.domain :as d]))

(defn hash-url-and-save
  [save-to-repo-fn url]
  (let [hash-key (d/hash-id (d/gen-id))]
    (save-to-repo-fn hash-key url)
    hash-key))

(defn get-original-url
  [get-from-repo-fn hash-key]
  (get-from-repo-fn hash-key))
