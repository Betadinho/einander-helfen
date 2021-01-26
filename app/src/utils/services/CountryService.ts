import axios from 'axios';

class CountryService {
    private baseUrl = searchURI;
    public countries: string[] = [];

    /**
     * The constructor initializes the `country` list.
     */
    constructor() {
        this.findCountries();
    }

    /**
     * This method finds all unique countries.
     */
    public findCountries():void {
        const query = {
            "size": 0,
            "aggs": {
                "country": {
                    "terms": { "field": "post_struct.location.country.keyword" }
                }
            }
        }

        this.performQuery(query);
    }

    /**
     * This method performs the elasticsearch query
     * @param query The elasticsearch querystring
     */
    private performQuery(query: any): Promise<any> {
        return new Promise<any>((resolve, reject) => {
            axios.post(this.baseUrl, query)
                .then(({ data }) => {
                    data.aggregations.country.buckets.map((elem: any) => {
                        if (elem.key !== "Deutschland") {
                            this.countries.push(elem.key);
                        }
                    });
                })
                .catch((error) => reject(error));
        });
    }
}

const countryServiceInstance = new CountryService();

export default countryServiceInstance;

export {
    countryServiceInstance as CountryService,
};