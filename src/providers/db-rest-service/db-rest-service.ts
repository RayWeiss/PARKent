import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

/*
  Generated class for the DbRestServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class DbRestServiceProvider {
  response: any;
  data: any;
  getSpotsResponse: any;
  getStatusResponse: any;
  getAllStatusResponse: any;

  constructor(public http: Http) {
    console.log('Hello DbRestServiceProvider Provider');
  }

  getSpots() {
    // if (this.getSpotsResponse) {
    //     // already loaded data
    //     return Promise.resolve(this.getSpotsResponse);
    //   }
      // don't have the data yet
      return new Promise(resolve => {
        // We're using Angular HTTP provider to request the data,
        // then on the response, it'll map the JSON data to a parsed JS object.
        // Next, we process the data and resolve the promise with the new data.
        this.http.get('http://127.0.0.1:5000/allLots')
          .map(res => res.json())
          .subscribe(data => {
            // we've got back the raw data, now generate the core schedule data
            // and save the data for later reference
            this.getSpotsResponse = data;
            resolve(this.getSpotsResponse);
          });
      });
    }

    getStatus(lotName) {
      // if (this.getStatusResponse) {
      //     // already loaded data
      //     return Promise.resolve(this.getStatusResponse);
      //   }
        // don't have the data yet
        return new Promise(resolve => {
          // We're using Angular HTTP provider to request the data,
          // then on the response, it'll map the JSON data to a parsed JS object.
          // Next, we process the data and resolve the promise with the new data.
          this.http.get('http://127.0.0.1:5000/percentleft/' + lotName)
            .map(res => res.json())
            .subscribe(data => {
              // we've got back the raw data, now generate the core schedule data
              // and save the data for later reference
              this.getStatusResponse = data;
              resolve(this.getStatusResponse);
            });
        });
      }

      getAllStatus() {
        // if (this.getStatusResponse) {
        //     // already loaded data
        //     return Promise.resolve(this.getStatusResponse);
        //   }
          // don't have the data yet
          return new Promise(resolve => {
            // We're using Angular HTTP provider to request the data,
            // then on the response, it'll map the JSON data to a parsed JS object.
            // Next, we process the data and resolve the promise with the new data.
            this.http.get('http://127.0.0.1:5000/allStatus')
              .map(res => res.json())
              .subscribe(data => {
                // we've got back the raw data, now generate the core schedule data
                // and save the data for later reference
                this.getAllStatusResponse = data;
                resolve(this.getAllStatusResponse);
              });
          });
        }
    // getStuff() {
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
