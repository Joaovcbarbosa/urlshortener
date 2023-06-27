(ns url-shortener.core
  (:require [ring.adapter.jetty :as ring-jetty]
            [url-shortener.routes :as routes]
            [url-shortener.datomicadapter :as da])
  (:gen-class))

(defn start []
  (da/create-db-and-schema)
  (ring-jetty/run-jetty routes/app {:port  5009
                                    :join? false}))

(defn -main
  [& args]
  (start))