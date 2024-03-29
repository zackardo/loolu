(function($) {
    /*
    Validation Singleton
    */
    var Validation = function() {
        var rules = {
            email : {
               check: function(value) {
                   
                   if(value)
                       return testPattern(value,".+@.+\..+",'');
                   return true;
               },
               msg : "Enter a valid e-mail address."
            },

            url : {
               check : function(value) {
                   if(value) {
                       return testPattern(value,
                                  "(https?://)?(.+\.)+.{2,4}(/.*)?", 'i');
                   }
                   return true;
               },
               msg : "Enter a valid URL."
            },

            required : {
               check: function(value) {
                   if(value)
                       return true;
                   else
                       return false;
               },
               msg : "This field is required."
            }
        };

        var testPattern = function(value, pattern, opt) {
            var regExp = new RegExp("^"+pattern+"$",opt);
            return regExp.test(value);
        };

        return {
            addRule : function(name, rule) {
                rules[name] = rule;
            },

            getRule : function(name) {
                return rules[name];
            }
        }
    }
    
    /* 
    Form factory 
    */
    var Form = function(form) {
        var fields = [];
        form.find("input[validation], textarea[validation]").each(function() {
            fields.push(new Field(this));
        });
        this.fields = fields;
    }
    Form.prototype = {
        validate : function() {
            for(field in this.fields) {
                this.fields[field].validate();
            }
        },
        isValid : function() {
            for(field in this.fields) {
                if(!this.fields[field].valid) {
                    this.fields[field].field.focus();
                    return false;
                }
            }
            return true;
        }
    }
    
    /* 
    Field factory 
    */
    var Field = function(field) {
        this.field = $(field);
        this.valid = false;
        this.attach("change");
    }
    Field.prototype = {
        attach : function(event) {
            var obj = this;
            if(event == "change") {
                obj.field.bind("change",function() {
                    return obj.validate();
                });
            }
            if(event == "keyup") {
                obj.field.bind("keyup",function(e) {
                    return obj.validate();
                });
            }
        },
        validate : function() {
            var obj = this,
                field = obj.field,
                errorClass = "errorlist",
                errorlist = $(document.createElement("ul")).addClass(errorClass),
                types = field.attr("validation").split(" "),
                container = field.parent(),
                errors = []; 
            
            field.prev(".errorlist").remove();
            for (var type in types) {
                var rule = $.Validation.getRule(types[type]);
                var value = $.trim(field.val());

                if(!rule.check(value)) {
                    container.addClass("error");
                    errors.push(rule.msg);
                }
            }
            if(errors.length) {
                field.before(errorlist.empty());
                for(error in errors) {
                
                    errorlist.append("<li>"+ errors[error] +"</li>");        
                }
                obj.valid = false;
            } 
            else {
                errorlist.remove();
                container.removeClass("error");
                obj.valid = true;
            }
        }
    }
    
    /* 
    Validation extends jQuery prototype
    */
    $.extend($.fn, {
        validation : function() {
            var validator = new Form($(this));
            $.data($(this)[0], 'validator', validator);
            
            $(this).bind("submit", function(e) {
                validator.validate();
                if(!validator.isValid()) {
                    e.preventDefault();
                }
            });
        },
        validate : function() {
            var validator = $.data($(this)[0], 'validator');
            if (!validator)
                return false;

            validator.validate();
            return validator.isValid();
            
        }
    });
    $.Validation = new Validation();
})(jQuery);

