import { Component, ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams, Slides } from 'ionic-angular';
import { Chart } from 'chart.js';
import { DbRestServiceProvider } from '../../providers/db-rest-service/db-rest-service';

var chartType = 'bar';
var xLabel = ["9am","9:15am","9:30am","9:45am",
              "10am","10:15am","10:30am","10:45am",
              "11am","11:15am","11:30am","11:45am",
              "12pm","10:15pm","10:30pm","10:45pm",
              "1pm","1:15pm","1:30pm","1:45pm",
              "2pm","2:15pm","2:30pm","2:45pm",
              "3pm","3:15pm","3:30pm","3:45pm",
              "4pm","4:15pm","4:30pm","4:45pm",
              "5pm","5:15pm","5:30pm","5:45pm",
              "6pm","6:15pm","6:30pm","6:45pm",
              "7pm","7:15pm","7:30pm","7:45pm",
              "8pm","8:15pm","8:30pm","8:45pm",
              "9pm"]
var legendLabel = "Busy Times";
var blue = "rgb(77, 148, 255)";
Chart.defaults.global.maintainAspectRatio = true;
var showYAxis = false;
var beginAtZeroYAxis = true;
var maxYAxis = 1.0;

@IonicPage({
  name: 'DetailPage'
})
@Component({
  selector: 'page-detail',
  templateUrl: 'detail.html',
})

export class DetailPage {
  @ViewChild(Slides) slide: Slides;
  @ViewChild('mondayChart') mondayChart;
  @ViewChild('tuesdayChart') tuesdayChart;
  @ViewChild('wednesdayChart') wednesdayChart;
  @ViewChild('thursdayChart') thursdayChart;
  @ViewChild('fridayChart') fridayChart;
  @ViewChild('saturdayChart') saturdayChart;
  @ViewChild('sundayChart') sundayChart;

  barChart: any;
  lot: any;
  item: any;
  db: any;
  allPredictions: any[];
  imgURL = "/../../assets/images/";

  constructor(public navCtrl: NavController, public navParams: NavParams, public dbService: DbRestServiceProvider) {
    this.allPredictions = [];
    this.item = navParams.get('item');
    this.barChart = ["mondayChart", "tuesdayChart", "wednesdayChart", "thursdayChart", "fridayChart", "saturdayChart", "sundayChart"];
    this.lot = [this.item.lotName];
    this.db = dbService;
    this.imgURL += this.lot + ".JPG";
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad DetailPage');
    this.db.getPredictionsFor(this.item.lotName)
    .then(response => {
      for (var val in response) {
        console.log(response[val][0]);
        this.allPredictions.push(response[val][0]);
      }
    }).then(response => {
      this.initializeCharts();
    });
  }

  initializeCharts() {
    //Monday
    this.mondayChart = new Chart(this.mondayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(0,47),
          label: legendLabel,
          backgroundColor: blue,
        }]
      }
    }),

    //Tuesday
    this.tuesdayChart = new Chart(this.tuesdayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(49,97),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Wednesday
    this.wednesdayChart = new Chart(this.wednesdayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(98,146),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Thursday
    this.thursdayChart = new Chart(this.thursdayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(147,195),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Friday
    this.fridayChart = new Chart(this.fridayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(196,244),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Saturday
    this.saturdayChart = new Chart(this.saturdayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(245,293),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    });

    //Sunday
    this.sundayChart = new Chart(this.sundayChart.nativeElement, {
      type: chartType,
      options: {
        scales: {
          yAxes: [{
            display: showYAxis,
            ticks: {
                beginAtZero: beginAtZeroYAxis,
                max: maxYAxis
            }
          }],
        }
      },
      data: {
        labels: xLabel,
        datasets: [{
          data: this.allPredictions.slice(294,342),
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    });
  }

}
