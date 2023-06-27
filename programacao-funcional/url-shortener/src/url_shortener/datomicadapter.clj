(ns url-shortener.datomicadapter
  (:require [datomic.api :as d]))

(def conn (atom nil))

(def db-uri "datomic:mem://foo")

(def url-schema [{:db/ident :url/hash
                  :db/valueType :db.type/string
                  :db/cardinality :db.cardinality/one}
                 {:db/ident :url/long
                  :db/valueType :db.type/string
                  :db/cardinality :db.cardinality/one}])

(defn create-db-and-schema []  
  (d/create-database db-uri)
  (reset! conn (d/connect db-uri))
  (d/transact @conn url-schema))

(defn save-to-datomic
  [key value]
  (d/transact @conn [{:db/id (d/tempid :db.part/user)
                      :url/hash key
                      :url/long value}]))


(defn get-from-datomic
  [hash]
  (let [db (d/db @conn)
        query '[:find ?long
                :in $ ?hash
                :where
                [?e :url/hash ?hash]
                [?e :url/long ?long]]
        result (d/q query db hash)]
    (if-let [[long-url] (first result)]
      long-url
      nil)))
