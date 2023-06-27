(ns url-shortener.routes
  (:require [reitit.ring :as ring]
            [muuntaja.core :as m]
            [reitit.ring.middleware.muuntaja :as muuntaja]
            [url-shortener.controllers :as c]))

(def app
  (ring/ring-handler
   (ring/router
    ["/"
     ["shorten" {:post c/shorten-url}]
     ["go/:hash-id" {:get c/redirect-to-original}]
     ["" {:get c/string-handler}]]
    {:data {:muuntaja m/instance
            :middleware [muuntaja/format-middleware]}})))