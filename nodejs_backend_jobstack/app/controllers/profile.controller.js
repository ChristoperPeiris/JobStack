const db = require("../models");
const userCompany = db.usercompany;
const User = db.user;
const companyTable = db.company;
const request = require('request');
// var querystring = require('querystring');


exports.getRecommendations = (req, res) => {
    var id = req.params.id;
    var list = "";
    var company;
    var companyD;
    var companyData = [];

    User.findOne({
        where: {
          userId: id
        }
      })
        .then(user => {
          if (!user) {
            return res.status(404).send({ message: "User Not found." });
          }

          const options ={
            url: 'http://127.0.0.1:5000/recommend',
            json: true,
            body: {
               cdskill : "ck" + user.codingSkill,
               scskill : "sk" + user.socialSkill,
               lsskill : "ls" + user.languageSkill,
               pdskill : "pd" + user.programDevelopment,
               degree : user.degreeId,
               feskil : "fe" + user.frontEndDevelopment,
               beskill : "be" + user.backEndDevelopment,
               fsskill : "fs" + user.fullStack,
               mdskill :"md" + user.mobileDevelopment,
               wdskill : "wd" + user.webDevelopment,
               uskill : "u" + user.uiUx
            }
          };

          request.post(options,
            (error, resc, body) => {
                if(error) {
                    console.error(error);
                    return;
                }
                company = JSON.stringify(body).split('"');
                for (x in company){
                  if(company[x].includes("CID")){
                    list = list + (company[x] + ",");
                  }
                }
                console.log(list);

                companyD = list.split(",");
                for(i=0; i<(companyD.length-1);i++){
                  userCompany.create({
                    companyId: companyD[i],
                    userId: id
                  });
                }

            companyD = list.split(",");
            for(i=0; i<(companyD.length-1);i++){
              console.log(i);
              companyTable.findOne({
                where:{
                   companyId: companyD[i]
                }
              }
            )
            .then(msg => {
              console.log(msg.companyName);
              companyData.push(msg.companyName);
            }).catch(err => {
              console.log(err);
              res.status(500).send({ message: err.message });
            });
           }
           
           console.log(companyData);
           res.send({companyData});
          });
        })
        .catch(err => {
          console.log(err);
          res.send({ message: err.message });
        });
};