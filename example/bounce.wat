(module
    (memory (export "memory") 1)
    (global $pos_x_addr i32 (i32.const 0))  ;; Component data from the engine

    (global $vel_x_addr i32 (i32.const 0x24))  ;; User script data

    (global $left_bound f64 (f64.const 0))  ;; Constants
    (global $right_bound f64 (f64.const 15))

    ;; Called once at the start
    (func (export "setup")
	;; Set initial velocity
        (f64.store (global.get $vel_x_addr) (f64.const 4))
    )

    ;; Called repeatedly, once per engine update
    (func (export "update") (param $dt f64) (local $vel_x f64)
	;; Load previous velocity from memory
        (local.set $vel_x (f64.load (global.get $vel_x_addr)))

	;; Flip velocity if position has reached bounds
        (local.set $vel_x
            (select
                (f64.abs (local.get $vel_x))
                (local.get $vel_x)
		(f64.le
		    (f64.load (global.get $pos_x_addr))
		    (global.get $left_bound)
		)
            )
        )
        (local.set $vel_x
            (select
                (f64.neg (f64.abs (local.get $vel_x)))
                (local.get $vel_x)
		(f64.ge
		    (f64.load (global.get $pos_x_addr))
		    (global.get $right_bound)
		)
            )
        )

        ;; Store velocity back to memory
        (f64.store (global.get $vel_x_addr) (local.get $vel_x))

        ;; Update position using velocity and delta time
        (f64.store (global.get $pos_x_addr)
            (f64.add
                (f64.load (global.get $pos_x_addr))
                (f64.mul
                    (local.get $vel_x)
                    (local.get $dt)
                )
            )
        )
    )
    (func (export "icantread") (result f64)
	(f64.load (global.get $pos_x_addr))
    )
)
