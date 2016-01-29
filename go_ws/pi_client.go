// Copyright 2015 The Gorilla WebSocket Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// +build ignore

package main

import (
	"flag"
	"log"
	"math/rand"
	"net/url"
	"os"
	"os/signal"
	"strconv"
	"time"

	"github.com/gorilla/websocket"
)

// engr2-2-79-150-dhcp:pi_python andrewgordon$ gcloud compute instances list
// NAME      ZONE          MACHINE_TYPE  PREEMPTIBLE INTERNAL_IP EXTERNAL_IP     STATUS
// pi-server us-central1-a n1-standard-1             10.240.0.2  130.211.133.242 RUNNING

const (
	GcloudIp = "104.154.67.221:8080"
)

// var addr = flag.String("addr", GOOGLE_CLOUD_IP + ":" + GOOGLE_CLOUD_PORT, "http service address")
var addr = flag.String("addr", GcloudIp, "http service address")

func main() {

	flag.Parse()
	log.SetFlags(0)

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)
	u := url.URL{Scheme: "ws", Host: *addr, Path: "/echo"}
	log.Printf("connecting to %s", u.String())

	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	done := make(chan struct{})

	go func() {
		defer c.Close()
		defer close(done)
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				log.Println("read:", err)
				return
			}
			log.Printf("recv: %s", message)
		}
	}()

	ticker := time.NewTicker(time.Second * 5)
	defer ticker.Stop()

	var r int
	var m string
	var message string

	for {
		select {
		case t := <-ticker.C:

			//read data from a sensor here
			r = rand.Int()
			m = strconv.Itoa(r)
			message = t.String() + "       " + m
			message = m

			err := c.WriteMessage(websocket.TextMessage, []byte(message))
			if err != nil {
				log.Println("write:", err)
				return
			}
		case <-interrupt:
			log.Println("interrupt:", interrupt)
			// To cleanly close a connection, a client should send a close
			// frame and wait for the server to close the connection.

			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Println("write close:", err)
				return
			}
			select {
			case <-done:
			case <-time.After(time.Second):
			}
			c.Close()
			return
		}
	}
}
