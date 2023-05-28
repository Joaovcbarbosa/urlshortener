(ns url-shortener-api.core
  (:require [ring.adapter.jetty :as ring-jetty]
            [reitit.ring :as ring]
            [muuntaja.core :as m]
            [reitit.ring.middleware.muuntaja :as muuntaja]
            [url-shortener-api.utils :as utils]) 
  (:gen-class))

(def urls (atom []))

(defn string-handler [_]
  {:status 200
   :body "url shortener"})

(defn create-url [{body :body-params}]
  (let [id (utils/gen-id) 
        long-url (:long-url body)
        existing-url (some #(= long-url (:long-url %)) @urls)]
    (if existing-url
      {:status 200
       :body (deref urls)}
      (do
        (swap! urls conj {:id id :long-url long-url :short-url (utils/hash-id id)}) 
        {:status 201
         :body (deref urls)}))))

(defn get-urls [_]
  {:status 200
   :body @urls})

(defn get-long-url [{{:keys [short-url]} :path-params}]
  (let [url (first (filter #(= short-url (:short-url %)) @urls))]
    (if url
      {:status 301
       :headers {"Location" (:long-url url)}}
      {:status 404
       :body "404 - Not Found. A url informada não consta no repositório de URLs"})))

(def app
  (ring/ring-handler
   (ring/router
    ["/"
     ["" string-handler]
     ["favicon.ico" {:get (fn [_] {:status 404 :body ""})}]
     ["urls/:short-url" get-long-url]
     ["urls" {:get get-urls
              :post create-url}]]
    {:data {:muuntaja m/instance
            :middleware [muuntaja/format-middleware]}})))

(defonce server (atom nil))

(defn start []
  (reset! server (ring-jetty/run-jetty app {:port 3000 :join? false})))

(defn stop []
  (when @server
    (.stop @server)))

(defn -main
  [& args]
  (start))
