import Location from '@/models/location';

class LocationService {
    private locations: Location[] = [];
    private selectedLocationAmount = 10;

    /**
     * The constructor initializes the `Location` list.
     */
    constructor() {
        this.loadLocationCsv('@/public/files/cities_lat_lon.csv');
    }

    /**
     * This method executes a query on on the locations specified by a string.
     * If there is not input or a * the wildcard query is executed.
     * Otherwise it searches for `Location`s where the name or plz starts with the input string.
     * @param searchValue   The input string for the query.
     * @returns A list of top `this.selectedLocationAmount` `Location`s ordered by rank and name.
     */
    public findLocationByPlzOrName(searchValue: string): Location[] {
        // call wildcard query if searchValue is null or empty
        if (!searchValue || searchValue === '' || searchValue === '*') {
            return this.findLocationWildcard();
        }

        // get locations which start with the searchValue string
        const selectedLocations = [] as Location[];
        console.log(this.locations);
        this.locations.forEach((location) => {
            if (location.name.startsWith(searchValue) ||
                location.plz.startsWith(searchValue)) {
                selectedLocations.push(location);
            }
        });
        selectedLocations.sort(this.dynamicSort('rank'));

        return selectedLocations.splice(0, this.selectedLocationAmount);
    }
    /**
     * This method executes a wildcard query on the locations.
     * @returns A list of top `this.selectedLocationAmount` `Location`s ordered by rank and name.
     */
    private findLocationWildcard(): Location[] {
        const selectedLocations = [] as Location[];
        this.locations.forEach((location) => {
            selectedLocations.push(location);
        });
        selectedLocations.sort(this.dynamicSort('rank'));

        return selectedLocations.splice(0, this.selectedLocationAmount);
    }

    /**
     * This method helps to sort any list of object by a specific property.
     * The method needs to be call inside of a `<T>.sort(dynamicSort('abc'))` method.
     * @param property  The property the object should be sorted by.
     * @returns A number between -1 - 1:
     *          - -1:   b comes before a.
     *          - 0:    a and b are equal.
     *          - 1:    a comes before b.
     */
    private dynamicSort(property): any {
        return (a, b) => {
            return (a[property] < b[property] ? -1 :
                (a[property] > b[property]) ? 1 : 0);
        };
    }


    /**
     * This method loads a CSV file and stores the content as `Location` in locations.
     * @param csvFile The CSV input file
     */
    private loadLocationCsv(csvFile): void {
        // TODO load csv file and save values to locations
        for (let i = 0; i < 15; i++) {
            this.locations.push({
                name: 'Frankfurt ' + i,
                plz: i + '6592',
                state: 'Hessen',
                lat: i * 3.0,
                lon: i * 2.0,
                rank: i % 10
            });
        }
    }
}

const locationServiceInstance = new LocationService();

export default locationServiceInstance;

export {
    locationServiceInstance as LocationService,
};
