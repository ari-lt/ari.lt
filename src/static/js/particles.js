/*
 * @licstart The following is the entire license notice for the JavaScript code in this file.
 *
 * Copyright (C) 2024 Ari Archer
 *
 * This file is part of ari.lt.
 *
 * The JavaScript code in this file is free software: you can redistribute it
 * and/or modify it under the terms of the GNU Affero General Public License
 * (AGPL) as published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version. The code is distributed WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
 *
 * As additional permission under AGPL version 3 section 7, you may distribute non-source
 * (e.g., minimized or compacted) forms of that code without the copy of the AGPL normally
 * required by section 4, provided you include this license notice and a URL through which
 * recipients can access the Corresponding Source.
 *
 * @licend The above is the entire license notice for the JavaScript code in this file.
 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.createElement("canvas");
    canvas.id = "particles";
    document.body.prepend(canvas);

    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let particles = [];
    const particle_density = 2e-5;
    let num_particles;

    const particle_size = 2;
    const avoidance_radius = 64;
    const connection_radius = 192;

    let mouse = {
        x: -1,
        y: -1,
    };

    let animation_frame_id = null;

    function update_pointer(e) {
        if (e.touches) {
            mouse.x = e.touches[0].clientX;
            mouse.y = e.touches[0].clientY;
        } else {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        }
    }

    function debounce(func, wait, immediate) {
        let timeout;
        return function () {
            let context = this,
                args = arguments;
            let later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            let call_now = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (call_now) func.apply(context, args);
        };
    }

    window.addEventListener("mousemove", update_pointer);
    window.addEventListener("touchmove", update_pointer);

    window.addEventListener(
        "resize",
        debounce(() => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            cancelAnimationFrame(animation_frame_id);
            init();
            animate();
        }, 250),
    );

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.velocity = {
                x: (Math.random() - 0.5) * 2,
                y: (Math.random() - 0.5) * 2,
            };
        }

        update() {
            if (this.x <= 0 || this.x >= canvas.width) {
                this.velocity.x *= -1;
                this.x = Math.max(Math.min(this.x, canvas.width), 0);
            }

            if (this.y <= 0 || this.y >= canvas.height) {
                this.velocity.y *= -1;
                this.y = Math.max(Math.min(this.y, canvas.height), 0);
            }

            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < avoidance_radius && distance > 0) {
                this.velocity.x += (dx / distance) * 0.5;
                this.velocity.y += (dy / distance) * 0.5;
            }

            this.x += this.velocity.x;
            this.y += this.velocity.y;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, particle_size, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(255, 81, 71, 0.5)";
            ctx.fill();
        }
    }

    function draw_connections() {
        particles.forEach((particle, idx) => {
            for (let i = idx + 1; i < particles.length; i++) {
                let other_particle = particles[i];
                let dx = other_particle.x - particle.x;
                let dy = other_particle.y - particle.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connection_radius) {
                    ctx.strokeStyle = `rgba(255, 81, 71, ${1 - distance / connection_radius})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particle.x, particle.y);
                    ctx.lineTo(other_particle.x, other_particle.y);
                    ctx.stroke();
                }
            }
        });
    }

    function init() {
        particles = [];
        num_particles = Math.floor(
            particle_density * canvas.width * canvas.height,
        );
        num_particles = Math.min(num_particles, 1024);
        for (let i = 0; i < num_particles; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach((particle) => {
            particle.update();
            particle.draw();
        });
        draw_connections();
        animation_frame_id = requestAnimationFrame(animate);
    }

    init();
    animate();
});
