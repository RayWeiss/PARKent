import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { DbRestServiceProvider } from '../../providers/db-rest-service/db-rest-service';
import { Observable } from 'rxjs/Rx';

@IonicPage()
@Component({
  selector: 'page-list',
  templateUrl: 'list.html',
  providers: [DbRestServiceProvider]
})

export class ListPage {
  items: any[];
  db: any;

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.db = dbService;
    this.items = [];

    this.initializeCounts();
    this.continuallyUpdateCounts();
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ListPage');
  }

  itemSelected(item) {
    this.navCtrl.push('DetailPage', {
      item: item
    });
  }

  initializeCounts() {
    this.db.getFracLeft()
    .then(response => {
      for (var val in response) {
        var spots = response[val];
        for (var spot in spots) {
          var lotName = spot;
          var fracValues = spots[spot];
          var spotsLeft = fracValues[0];
          var totalSpots = fracValues[1];
          this.items.push({
            lotName: lotName,
            spotsLeft: spotsLeft,
            totalSpots: totalSpots
          });
        }
      }
    });
  }

  continuallyUpdateCounts() {
    const seconds = 1;
    const interval = Observable.interval(seconds * 1000);
    const forever = interval.filter(val => false);

    interval.takeUntil(forever).subscribe(val => {
      var tempArr = [];
      this.db.getFracLeft()
      .then(response => {
        for (var val in response) {
          var spots = response[val];
          for (var spot in spots) {
            var lotName = spot;
            var fracValues = spots[spot];
            var spotsLeft = fracValues[0];
            var totalSpots = fracValues[1];
            tempArr.push({
              lotName: lotName,
              spotsLeft: spotsLeft,
              totalSpots: totalSpots
            });
          }
        }
      }).then(response => {
        this.items = tempArr;
      });
    });

  }

}
