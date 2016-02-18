package influx

import (
	"fmt"
	"log"
	"net/url"
	"os"

	"github.com/influxdb/influxdb/client/v2"
)

const (
	DB                = "sensor_data"
	USER              = "sensor_root"
	AUTH              = "horn"
	SENSOR_COLLECTION = "sensor_house"
	INFLUX_URL_LOCAL  = "http://localhost:8086"
)

var out = log.New(os.Stderr, "weave:services:influx ", log.LstdFlags)

func checkError(err error) {
	if err != nil {
		fmt.Println("Erorr on", err)
	}
}

func QueryInfluxDB(clnt client.Client, cmd string) (res []client.Result, err error) {

	q := client.Query{
		Command:  cmd,
		Database: DB,
	}

	if response, err := clnt.Query(q); err == nil {
		if response.Error() != nil {
			return res, response.Error()
		}
		res = response.Results
	}

	return res, nil
}

func DropCollection(clnt client.Client, name string) (res []client.Result, err error) {

	q := client.Query{
		Command:  "drop measurement " + name,
		Database: DB,
	}

	if response, err := clnt.Query(q); err == nil {
		if response.Error() != nil {
			return res, response.Error()
		}
		res = response.Results
	}
	return res, nil
}

func main() {

	u, _ := url.Parse(INFLUX_URL_LOCAL)
	out.Println("Connected to", u)

	client := client.NewClient(client.Config{
		URL:      u,
		Username: USER,
		Password: AUTH,
	})

	r, err := QueryInfluxDB(client, "select * from sensor_house")
	if err != nil {
		fmt.Println("r =", r)
	}
}
