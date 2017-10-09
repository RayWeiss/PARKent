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

  constructor(public http: Http) {
    this.response = this.http.get('http://127.0.0.1:5000/allLots');
    this.response.subscribe(
        data => {
            console.log(data);
            console.log(data._body)
            // console.log(data.data);
            // this.response = data.data.children;
        },
        err => {
            console.log("Oops!");
        }
    );
    console.log('Hello DbRestServiceProvider Provider');
  }

}
