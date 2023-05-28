(ns url-shortener-api.core
  (:require [ring.adapter.jetty :as ring-jetty]
            [reitit.ring :as ring]
            [muuntaja.core :as m]
            [reitit.ring.middleware.muuntaja :as muuntaja])
  (:gen-class))

" * '/' Retrun string on base URL"
" * '/urls' Return list of urls"
" * '/urls/:id Return url for a specific id"
" * '/urls POST a url"
(require '[clojure.set :as set])

(defn digits [n]
  (->> n str (map (comp read-string str))))

(defn reverse-str
  [my-str]
  (apply str (reverse my-str)))

(defn hash-id
  [n]
  (let [symbolmap (zipmap (concat
                           (map char (range 48 58))
                           (map char (range 97 123))
                           (map char (range 65 91)))
                          (range 62))]
    (loop [decNumber n
           result []]
      (if (= decNumber 0)
        (reverse-str result)
        (recur (quot decNumber 62)
               (conj result ((set/map-invert symbolmap) (mod decNumber 62))))))))

(defn gen-id []
  (rand-int 350000000))


;=====================================================
(def urls (atom []))

(defn string-handler [_]
  {:status 200
   :body "on the code again"})

(defn create-url [{body :body-params}]
  (let [id (gen-id)
        long-url (:long-url body)
        existing-url (some #(= long-url (:long-url %)) @urls)]
    (when-not existing-url
      (swap! urls conj {:id id :long-url long-url :short-url (hash-id id)}))
    {:status 201
     :body (deref urls)}))

(defn get-urls [_]
  {:status 200
   :body @urls})

(defn get-long-url [{{:keys [short-url]} :path-params}]
  (let [url (first (filter #(= short-url (:short-url %)) @urls))]
    (if url
      {:status 200
        :body (:long-url url)}
      {:status 404
       :body "404 - not found"})))

(def app
  (ring/ring-handler
   (ring/router
    ["/"
     ["urls/:short-url" get-long-url]
     ["urls" {:get get-urls
               :post create-url}]
     ["" string-handler]]
    {:data {:muuntaja m/instance
            :middleware [muuntaja/format-middleware]}})))

(defonce server (atom nil))

(defn start []
  (reset! server (ring-jetty/run-jetty app {:port 1005 :join? false})))

(defn stop []
  (when @server
    (.stop @server)))

(defn -main
  [& args]
  (start))
