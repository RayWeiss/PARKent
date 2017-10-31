import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class DbRestServiceProvider {
  response: any;
  data: any;
  getSpotsResponse: any;
  getAllStatusResponse: any;
  getFracLeftResponse: any;

  // local
  host = 'http://127.0.0.1';
  port = ':5000';

  // // remote
  // host = 'http://131.123.35.143';
  // port = '5000';

  constructor(public http: Http) {
    console.log('Hello DbRestServiceProvider Provider');
  }

  getSpots() {
      return new Promise(resolve => {
        this.http.get(this.host + this.port + '/allLots')
          .map(res => res.json())
          .subscribe(data => {
            this.getSpotsResponse = data;
            resolve(this.getSpotsResponse);
          });
      });
    }

    getAllStatus() {
        return new Promise(resolve => {
          this.http.get(this.host + this.port + '/allStatus')
            .map(res => res.json())
            .subscribe(data => {
              this.getAllStatusResponse = data;
              resolve(this.getAllStatusResponse);
            });
        });
    }

    getFracLeft() {
        return new Promise(resolve => {
          this.http.get(this.host + this.port + '/fracLeft')
            .map(res => res.json())
            .subscribe(data => {
              this.getFracLeftResponse = data;
              resolve(this.getFracLeftResponse);
            });
        });
    }
    // templateCall1() {
    //   // if (this.getSpotsResponse) {
    //   //     // already loaded data
    //   //     return Promise.resolve(this.getSpotsResponse);
    //   //   }
    //     // don't have the data yet
    //     return new Promise(resolve => {
    //       // We're using Angular HTTP provider to request the data,
    //       // then on the response, it'll map the JSON data to a parsed JS object.
    //       // Next, we process the data and resolve the promise with the new data.
    //       this.http.get('http://127.0.0.1:5000/allLots')
    //         .map(res => res.json())
    //         .subscribe(data => {
    //           // we've got back the raw data, now generate the core schedule data
    //           // and save the data for later reference
    //           this.getSpotsResponse = data;
    //           resolve(this.getSpotsResponse);
    //         });
    //     });
    //   }

    // templateCall2() {
    //   this.response = this.http.get('http://127.0.0.1:5000/allLots');
    //   this.response.subscribe(
    //       data => {
    //           // console.log(data);
    //           console.log(data._body)
    //           // console.log(data.data);
    //           // this.response = data.data.children;
    //       },
    //       err => {
    //           console.log("Oops!");
    //       }
    //   );
    // }
}
