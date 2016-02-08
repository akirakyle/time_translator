var elements = document.getElementsByTagName('*');

function done_trans_callback(data, status) {
    console.log('Data: ' + data + '\nStatus: ' + status);
    console.log("i: " + data.i + " j: " + data.j + " text: " + data.text);
    node = elements[data.i].childNodes[data.j]
    console.log(node)
    var replacedText = data.text
    elements[data.i].replaceChild(document.createTextNode(replacedText), node);
}

console.log('sanitycheck')
for (var i = 0; i < elements.length; i++) {
    var element = elements[i];

    for (var j = 0; j < element.childNodes.length; j++) {
        var node = element.childNodes[j];

        if (node.nodeType === 3) {
            var text = node.nodeValue;

            $.post('http://spot.aikokyle.com/time_translate',
                {
                    i: i,
                    j: j,
                    text: text
                },
                   done_trans_callback
                );
        }
    }
}
