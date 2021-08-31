let compare_years y_one y_two = 
	if y_one >= 50 && y_two >= 50 || y_one < 50 && y_two < 50
		then y_two - y_one
	else
		if y_two >= 50 then y_two - (y_one + 100)
		else (y_two + 100) - y_one
;;

exception ExceedsTimeRange;;

let combine_years y_one add =
	if add > 0 then add_years y_one add
	else if add < 0 then sub_years y_one add
	else y_one
;;

let rec add_years y_one add =
	let combine = y_one + add in 
	if y_one <= 49 && combine > 50 || add >= 100 then raise ExceedsTimeRange
	else if y_one >= 50 && combine >= 100 then add_years (combine - 100) 0
	else combine
;;

let rec sub_years y_one sub = 
	let combine = y_one + sub in 
	if y_one >= 50 && combine < 50 || sub <= -100 then raise ExceedsTimeRange
	else if y_one <= 49 && combine < 0 then sub_years (combine + 100) 0
	else combine 
;;

let rec additive_mult x n =
	if n = 0 then 0.
	else if n > 0 then x +. additive_mult x (n - 1)
	else additive_mult x (n + 1) -. x
;;

let rec additive_mult_for x n =
	if n < 0 then additive_mult_for (-1. *. x) (-1 * n)
	else 
		let return = ref 0. in
		for i = 1 to n do
			return := x +. !return
		done;
		!return
;;