(function ($, undefined) {
    var gettext = window.gettext || function (val) {
        return val;
    };
    var $map, $foundLocations, $lat, $lng, $street, $street2,
        $city, $country, $postalCode, gMap, gMarker;

    function getAddress4search() {
        var sStreetAddress2 = $street2.val();
        if (sStreetAddress2) {
            sStreetAddress2 = " " + sStreetAddress2;
        }

        return [
            $street.val() + sStreetAddress2,
            $city.val(),
            $country.val(),
            $postalCode.val()
        ].join(", ");
    }

    function updateMarker(lat, lng) {
        var point = new google.maps.LatLng(lat, lng);

        if (!gMarker) {
            gMarker = new google.maps.Marker({
                position: point,
                map: gMap
            });
        }

        gMarker.setPosition(point);
        gMap.panTo(point, 15);
        gMarker.setDraggable(true);

        google.maps.event.addListener(gMarker, "dragend", function() {
            var point = gMarker.getPosition();
            updateLatitudeAndLongitude(point.lat(), point.lng());
        });
    }

    function updateLatitudeAndLongitude(lat, lng) {
        var precision = 1000000;
        $lat.val(Math.round(lng * precision) / precision);
        $lng.val(Math.round(lat * precision) / precision);
    }

    function autocompleteAddress(results) {
        var $item = $('<li/>');
        var $link = $('<a href="#"/>');

        $foundLocations.html("");
        results = results || [];

        if (results.length) {
            results.forEach(function (result, i) {
                $link.clone()
                     .html(result.formatted_address)
                     .click(function (event) {
                         event.preventDefault();
                         updateAddressFields(result.address_components);

                         var point = result.geometry.location;
                         updateLatitudeAndLongitude(
                             point.lat(), point.lng());
                         updateMarker(point.lat(), point.lng());
                         $foundLocations.hide();
                     })
                     .appendTo($item.clone().appendTo($foundLocations));
            });
            $link.clone()
                 .html(gettext("None of the above"))
                 .click(function(event) {
                     event.preventDefault();
                     $foundLocations.hide();
                 })
                 .appendTo($item.clone().appendTo($foundLocations));
        } else {
            $foundLocations.hide();
        }
    }

    function updateAddressFields(addressComponents) {
        var streetName, streetNumber;
        var typeActions = {
            "locality": function(obj) {
                $city.val(obj.long_name);
            },
            "street_number": function(obj) {
                streetNumber = obj.long_name;
            },
            "route": function(obj) {
                streetName = obj.long_name;
            },
            "postal_code": function(obj) {
                $postalCode.val(obj.long_name);
            },
            "country": function(obj) {
                $country.val(obj.short_name);
            }
        };

        addressComponents.forEach(function(component) {
            var action = typeActions[component.types[0]];
            if (typeof action === "function") {
                action(component);
            }
        });

        if (streetName) {
            var streetAddress = streetName;
            if (streetNumber) {
                streetAddress += " " + streetNumber;
            }
            $street.val(streetAddress);
        }
    }

    $(function(){
        $map = $(".map");

        $foundLocations = $map.find("ul.locations").hide();
        $lat = $("#id_latitude");
        $lng = $("#id_longitude");
        $street = $("#id_street");
        $street2 = $("#id_street2");
        $city = $("#id_city");
        $country = $("#id_country");
        $postalCode = $("#id_postal_code");

        $map.find("button.locate-address")
            .click(function(event) {
                var oGeocoder = new google.maps.Geocoder();
                oGeocoder.geocode(
                    {address: getAddress4search()},
                    function (results, status) {
                        if (status === google.maps.GeocoderStatus.OK) {
                            autocompleteAddress(results);
                        } else {
                            autocompleteAddress(false);
                        }
                    }
                );
            });

        $map.find("button.remove-geo")
            .click(function() {
                $lat.val("");
                $lng.val("");
                gMarker.setMap(null);
                gMarker = null;
            });

        gMap = new google.maps.Map($map.find(".canvas").get(0), {
            scrollwheel: false,
            zoom: 16,
            center: new google.maps.LatLng(51.511214, -0.119824),
            disableDoubleClickZoom: true
        });

        google.maps.event.addListener(gMap, "dblclick", function(event) {
            var lat = event.latLng.lat();
            var lng = event.latLng.lng();
            updateLatitudeAndLongitude(lat, lng);
            updateMarker(lat, lng);
        });

        if ($lat.val() && $lng.val()) {
            updateMarker($lat.val(), $lng.val());
        }
    });
}(django.jQuery));
